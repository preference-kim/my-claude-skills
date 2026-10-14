#!/usr/bin/env python3
"""Exercise quota stopping and cancellation with synthetic children, without model calls."""

import argparse
import io
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import run_pilot

SCRATCH = None


class QuotaTests(unittest.TestCase):
    def tearDown(self):
        run_pilot.STOP.clear()

    def test_stop_scope(self):
        def event(**values):
            return {"type": "rate_limit_event", "rate_limit_info": values}
        self.assertIsNotNone(run_pilot.quota_stop_reason(event(status="rejected", rateLimitType="seven_day")))
        self.assertIsNotNone(run_pilot.quota_stop_reason(event(status="allowed", isUsingOverage=True)))
        self.assertIsNone(run_pilot.quota_stop_reason(event(status="allowed", rateLimitType="seven_day")))
        self.assertIsNone(run_pilot.quota_stop_reason(event(status="rejected", rateLimitType="model_capacity")))

    def test_codex_quota_scope(self):
        messages = [
            "You’ve hit your usage limit. Try again later.",
            "You've hit your usage limit. Upgrade your plan to continue.",
            "Quota exceeded. Check your plan and billing details.",
            "Your workspace is out of credits. Add credits to continue.",
            "Your workspace is out of credits. Ask your workspace owner to refill in order to continue.",
            "You hit your spend cap set in your workspace. Increase your spend cap to continue.",
            "You hit your spend cap set by the owner of your workspace. Ask an owner to increase your spend cap to continue.",
            "To use Codex with your ChatGPT plan, upgrade to Plus: https://chatgpt.com/explore/plus.",
        ]
        for message in messages:
            for event in ({"type": "error", "message": message},
                          {"type": "turn.failed", "error": {"message": message}}):
                with self.subTest(event=event):
                    self.assertIsNotNone(run_pilot.quota_stop_reason(event))
        for message in ["Selected model is at capacity. Please try a different model.",
                        "Flex capacity unavailable.", "Rate limit exceeded; retry after 1 second.",
                        "You’ve hit your usage limit for example-model. Switch to another model now.",
                        "A task response quoting: You’ve hit your usage limit."]:
            self.assertIsNone(run_pilot.quota_stop_reason({"type": "error", "message": message}))
        for event in [None, [], {"type": "error", "message": None},
                      {"type": "turn.failed", "error": "malformed"},
                      {"type": "item.completed", "message": messages[0]}]:
            self.assertIsNone(run_pilot.quota_stop_reason(event))

    def campaign_arguments(self, root):
        case = {"id": "probe", "kind": "audit", "prompt": "synthetic", "partition": "development"}
        (root / "cases.json").write_text(json.dumps([case]))
        for variant in ("A", "B", "C"):
            directory = root / "guidance" / variant
            directory.mkdir(parents=True)
            (directory / "probe.md").write_text("synthetic guidance")
        return ["run_pilot.py", "--cases", str(root / "cases.json"),
                "--guidance", str(root / "guidance"), "--output", str(root / "output"),
                "--runtime", "codex", "--model", "fixture", "--effort", "fixture",
                "--partition", "development"]

    def test_codex_quota_stops_campaign_but_transient_errors_do_not(self):
        events = [({"type": "error", "message": "You’ve hit your usage limit. Try again later."}, True),
                  ({"type": "turn.failed", "error": {"message": "Quota exceeded. Check your plan and billing details."}}, True),
                  ({"type": "error", "message": "Selected model is at capacity. Please try a different model."}, False)]
        for event, quota in events:
            with self.subTest(event=event), tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
                root = Path(directory)
                argv = self.campaign_arguments(root)
                fake = root / "fake.py"
                fake.write_text("import sys\nsys.stdin.read()\nprint(" + repr(json.dumps(event)) + ", flush=True)\nraise SystemExit(1)\n")
                real_popen = subprocess.Popen
                children = []
                def spawn(_command, **kwargs):
                    child = real_popen([sys.executable, str(fake)], **kwargs)
                    children.append(child)
                    return child
                # The isolation probe is deliberately stubbed; this tests scheduling only.
                with patch.object(sys, "argv", argv), patch.object(run_pilot, "codex_isolation", return_value=None), patch.object(run_pilot.subprocess, "Popen", side_effect=spawn):
                    result = run_pilot.main()
                records = json.loads((root / "output/summary.json").read_text())
                self.assertEqual(len(records), 6)
                self.assertTrue(all(child.poll() is not None for child in children))
                if quota:
                    self.assertEqual(result, 3)
                    self.assertLessEqual(len(children), 2)
                    self.assertTrue(any(record["status"] == "quota_stopped" for record in records))
                    self.assertGreaterEqual(sum(record["status"] == "not_started_campaign_stop" for record in records), 4)
                else:
                    self.assertEqual(result, 1)
                    self.assertEqual(len(children), 6)
                    self.assertFalse(run_pilot.STOP.is_set())

    @unittest.skipUnless(hasattr(os, "killpg"), "process groups require a POSIX runtime")
    def test_controller_interrupt_cancels_queue_and_reaps_children(self):
        for signum in (signal.SIGINT, signal.SIGTERM):
            with self.subTest(signal=signum):
                self.check_controller_interrupt(signum)

    @unittest.skipUnless(hasattr(os, "killpg"), "process groups require a POSIX runtime")
    def test_controller_reports_worker_cleanup_failure(self):
        self.check_controller_interrupt(signal.SIGTERM, cleanup_error=True)

    def check_controller_interrupt(self, signum, cleanup_error=False):
        with tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
            root = Path(directory)
            argv = self.campaign_arguments(root)
            markers = root / "children"
            markers.mkdir()
            release = root / "release"
            fake = root / "fake.py"
            fake.write_text("import os,sys,time\nfrom pathlib import Path\nsys.stdin.read()\n"
                            f"Path({str(markers)!r}, str(os.getpid())).touch()\n"
                            "deadline=time.monotonic()+10\n"
                            f"while not Path({str(release)!r}).exists() and time.monotonic()<deadline:\n time.sleep(0.02)\n")
            wrapper = root / "controller.py"
            cleanup = ("real_terminate=run_pilot.terminate_group\n"
                       "def terminate(process):\n real_terminate(process)\n raise RuntimeError('synthetic cleanup error')\n"
                       "run_pilot.terminate_group=terminate\n") if cleanup_error else ""
            wrapper.write_text("import signal,subprocess,sys\nfrom unittest.mock import patch\n"
                               f"sys.path.insert(0, {str(Path(run_pilot.__file__).parent)!r})\nimport run_pilot\n"
                               + cleanup +
                               "signal.signal(signal.SIGINT, signal.default_int_handler)\n"
                               "real_popen=subprocess.Popen\n"
                               f"def spawn(_command, **kwargs):\n return real_popen([sys.executable, {str(fake)!r}], **kwargs)\n"
                               f"sys.argv={argv!r}\n"
                               "with patch.object(run_pilot, 'codex_isolation', return_value=None), patch.object(run_pilot.subprocess, 'Popen', side_effect=spawn):\n"
                               " raise SystemExit(run_pilot.main())\n")
            with (root / "controller.log").open("w") as log:
                controller = subprocess.Popen([sys.executable, str(wrapper)], stdout=log, stderr=log, start_new_session=True)
                try:
                    deadline = time.monotonic() + 5
                    while len(list(markers.iterdir())) < 2 and controller.poll() is None and time.monotonic() < deadline:
                        time.sleep(0.02)
                    self.assertEqual(len(list(markers.iterdir())), 2)
                    controller.send_signal(signum)
                    # Verify cleanup while children still require termination;
                    # releasing them first could hide surviving process groups.
                    self.assertNotEqual(controller.wait(timeout=5), 0)
                    self.assertEqual(len(list(markers.iterdir())), 2)
                    records = [json.loads(path.read_text()) for path in (root / "output").glob("*/record.json")]
                    if cleanup_error:
                        self.assertIn("worker failures:", (root / "controller.log").read_text())
                        self.assertIn("synthetic cleanup error", (root / "controller.log").read_text())
                    else:
                        self.assertEqual(len(records), 2)
                        self.assertTrue(all(record["status"] == "campaign_stopped" and record["exit_code"] is not None for record in records))
                    for marker in markers.iterdir():
                        with self.assertRaises(ProcessLookupError):
                            os.killpg(int(marker.name), 0)
                finally:
                    release.touch()
                    for pid in [controller.pid, *(int(marker.name) for marker in markers.iterdir())]:
                        try:
                            os.killpg(pid, signal.SIGKILL)
                        except ProcessLookupError:
                            pass
                    controller.wait(timeout=3)

    def test_codex_prompt_inspection_without_tool_evidence_blocks_actors(self):
        with tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
            root = Path(directory)
            argv = self.campaign_arguments(root)
            inspected = SimpleNamespace(returncode=0, stdout="[]", stderr="")
            with patch.object(sys, "argv", argv), patch.object(run_pilot.subprocess, "run", return_value=inspected), patch.object(run_pilot, "run_one", side_effect=AssertionError("actor launch must be blocked")) as actor:
                result = run_pilot.main()
            self.assertEqual(result, 2)
            actor.assert_not_called()
            blocked = json.loads((root / "output/blocked.json").read_text())
            self.assertEqual(blocked["generations"], 0)
            self.assertIn("tool", blocked["reason"])

    def test_controller_restores_signal_handlers_after_failure(self):
        with tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
            argv = self.campaign_arguments(Path(directory))
            previous = {signum: signal.getsignal(signum) for signum in (signal.SIGINT, signal.SIGTERM)}
            with patch.object(sys, "argv", argv), patch.object(run_pilot, "codex_isolation", return_value=None), patch.object(run_pilot, "run_one", side_effect=RuntimeError("synthetic worker failure")):
                with self.assertRaisesRegex(RuntimeError, "synthetic worker failure"):
                    run_pilot.main()
            self.assertEqual({signum: signal.getsignal(signum) for signum in previous}, previous)

    def test_child_is_stopped_and_queued_work_skipped(self):
        with tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
            root = Path(directory)
            guidance = root / "guidance/A"
            guidance.mkdir(parents=True)
            (guidance / "probe.md").write_text("synthetic guidance")
            fake = root / "fake.py"
            fake.write_text('import sys,json,time\nsys.stdin.read()\n'
                            'print(json.dumps({"type":"system","subtype":"init","skills":[],"plugins":[],"mcp_servers":[]}),flush=True)\n'
                            'print(json.dumps({"type":"rate_limit_event","rate_limit_info":{"status":"rejected","rateLimitType":"seven_day"}}),flush=True)\n'
                            'time.sleep(30)\n')
            args = SimpleNamespace(output=root, guidance=guidance.parent, runtime="claude", model="fixture", effort="fixture", fallback=None)
            case = {"id": "probe", "kind": "audit", "prompt": "synthetic"}
            real_popen = subprocess.Popen
            def spawn(_command, **kwargs):
                return real_popen([sys.executable, str(fake)], **kwargs)
            with patch.object(run_pilot.subprocess, "Popen", side_effect=spawn) as popen:
                record = run_pilot.run_one(args, case, "A", 1)
                self.assertEqual(record["status"], "quota_stopped")
                self.assertLess(record["elapsed_seconds"], 5)
                self.assertIsNotNone(record["exit_code"])
                later = run_pilot.run_one(args, case, "A", 2)
                self.assertEqual(later["status"], "not_started_campaign_stop")
                self.assertEqual(popen.call_count, 1)

    def test_stop_during_preparation_prevents_launch(self):
        with tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
            root = Path(directory)
            args = SimpleNamespace(output=root, guidance=root, runtime="claude", model="fixture", effort="fixture", fallback=None)
            case = {"id": "probe", "kind": "audit", "prompt": "synthetic"}
            def read_guidance(*_args, **_kwargs):
                run_pilot.stop_campaign()
                return "synthetic guidance"
            with patch.object(Path, "read_text", side_effect=read_guidance), patch.object(run_pilot.subprocess, "Popen") as popen:
                record = run_pilot.run_one(args, case, "A", 1)
            self.assertEqual(record["status"], "not_started_campaign_stop")
            popen.assert_not_called()

    def test_final_output_is_checked_before_accepting_completion(self):
        with tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
            root = Path(directory)
            (root / "A").mkdir()
            (root / "A/probe.md").write_text("synthetic guidance")
            args = SimpleNamespace(output=root, guidance=root, runtime="claude", model="fixture", effort="fixture", fallback=None)
            case = {"id": "probe", "kind": "audit", "prompt": "synthetic"}
            def spawn(_command, **kwargs):
                def poll():
                    kwargs["stdout"].write(json.dumps({"type": "rate_limit_event", "rate_limit_info": {"status": "rejected", "rateLimitType": "seven_day"}}) + "\n")
                    kwargs["stdout"].flush()
                    return 0
                return SimpleNamespace(stdin=io.StringIO(), poll=poll, returncode=0)
            with patch.object(run_pilot.subprocess, "Popen", side_effect=spawn), patch.object(run_pilot, "terminate_group"):
                record = run_pilot.run_one(args, case, "A", 1)
            self.assertEqual(record["status"], "quota_stopped")
            self.assertFalse(record["isolation_verified"])
            self.assertTrue(run_pilot.STOP.is_set())

    def test_signal_failure_still_attempts_bounded_reaping(self):
        for leader_exits in (True, False):
            waits = []
            def wait(timeout):
                waits.append(timeout)
                if not leader_exits:
                    raise subprocess.TimeoutExpired("fixture", timeout)
                return -15
            process = SimpleNamespace(pid=123, poll=lambda: None, wait=wait)
            with patch.object(run_pilot.os, "killpg", side_effect=PermissionError("synthetic EPERM")), patch.object(run_pilot, "TERMINATION_GRACE_SECONDS", 0.01):
                with self.assertRaisesRegex(RuntimeError, "termination unverified.*synthetic EPERM"):
                    run_pilot.terminate_group(process)
            self.assertEqual(waits, [0.01] * 3)

    def test_probe_permission_failure_is_not_group_absence(self):
        waits = []
        process = SimpleNamespace(pid=123, poll=lambda: None, wait=lambda timeout: waits.append(timeout))
        def signal_group(_pid, sig):
            if sig == 0:
                raise PermissionError("synthetic probe EPERM")
        with patch.object(run_pilot.os, "killpg", side_effect=signal_group), patch.object(run_pilot, "TERMINATION_GRACE_SECONDS", 0.01):
            with self.assertRaisesRegex(RuntimeError, "termination unverified.*probe EPERM"):
                run_pilot.terminate_group(process)
        self.assertEqual(waits, [0.01] * 3)

    def test_primary_failure_survives_cleanup_failure_and_stops_campaign(self):
        with tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
            root = Path(directory)
            (root / "A").mkdir()
            (root / "A/probe.md").write_text("synthetic guidance")
            args = SimpleNamespace(output=root, guidance=root, runtime="claude", model="fixture", effort="fixture", fallback=None)
            case = {"id": "probe", "kind": "audit", "prompt": "synthetic"}
            def poll():
                raise OSError("synthetic primary error")
            process = SimpleNamespace(poll=poll)
            with patch.object(run_pilot.subprocess, "Popen", return_value=process), patch.object(run_pilot, "terminate_group", side_effect=RuntimeError("synthetic cleanup error")):
                with self.assertRaisesRegex(RuntimeError, "primary error.*cleanup error") as caught:
                    run_pilot.run_one(args, case, "A", 1)
            self.assertIsInstance(caught.exception.__cause__, OSError)
            self.assertTrue(run_pilot.STOP.is_set())

    def test_unread_large_prompt_does_not_block_timeout(self):
        with tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
            root = Path(directory)
            (root / "A").mkdir()
            (root / "A/probe.md").write_text("synthetic guidance")
            args = SimpleNamespace(output=root, guidance=root, runtime="codex", model="fixture", effort="fixture", fallback=None)
            case = {"id": "probe", "kind": "audit", "prompt": "synthetic " * 100000}
            real_popen = subprocess.Popen
            def spawn(_command, **kwargs):
                return real_popen([sys.executable, "-c", "import time; time.sleep(10)"], **kwargs)
            with patch.object(run_pilot.subprocess, "Popen", side_effect=spawn), patch.object(run_pilot, "RUN_TIMEOUT_SECONDS", 0.1):
                record = run_pilot.run_one(args, case, "A", 1)
            self.assertEqual(record["status"], "timeout")
            self.assertIsNotNone(record["exit_code"])
            self.assertLess(record["elapsed_seconds"], 3)

    @unittest.skipUnless(hasattr(os, "fork"), "process groups require a POSIX runtime")
    def test_group_termination_outlives_leader(self):
        with tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
            root = Path(directory)
            fake = root / "descendant.py"
            fake.write_text('import os,signal,time\nfrom pathlib import Path\n'
                            'child=os.fork()\n'
                            'if child == 0:\n'
                            ' signal.signal(signal.SIGTERM, signal.SIG_IGN)\n'
                            ' Path("ready").write_text(str(os.getpid()))\n'
                            ' while True:\n'
                            '  Path("heartbeat").write_text(str(time.monotonic()))\n'
                            '  time.sleep(0.02)\n'
                            'else:\n'
                            ' time.sleep(30)\n')
            process = subprocess.Popen([sys.executable, str(fake)], cwd=root, start_new_session=True)
            try:
                deadline = time.monotonic() + 3
                while not (root / "heartbeat").exists() and time.monotonic() < deadline:
                    time.sleep(0.02)
                self.assertTrue((root / "heartbeat").exists())
                with patch.object(run_pilot, "TERMINATION_GRACE_SECONDS", 0.15):
                    run_pilot.terminate_group(process)
                time.sleep(0.1)
                heartbeat = (root / "heartbeat").read_text()
                time.sleep(0.1)
                self.assertEqual((root / "heartbeat").read_text(), heartbeat)
                self.assertIsNotNone(process.returncode)
            finally:
                try:
                    try:
                        os.killpg(process.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                finally:
                    process.wait(timeout=3)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scratch", type=Path, required=True)
    args, remaining = parser.parse_known_args()
    SCRATCH = args.scratch.resolve()
    SCRATCH.mkdir(parents=True, exist_ok=True)
    unittest.main(argv=[__file__, *remaining])
