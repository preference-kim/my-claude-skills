#!/usr/bin/env python3
"""Exercise quota stopping with a synthetic child process, without model calls."""

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
            process = SimpleNamespace(pid=123, wait=wait)
            with patch.object(run_pilot.os, "killpg", side_effect=PermissionError("synthetic EPERM")):
                with self.assertRaisesRegex(RuntimeError, "termination unverified.*synthetic EPERM"):
                    run_pilot.terminate_group(process)
            self.assertEqual(waits, [run_pilot.TERMINATION_GRACE_SECONDS])

    def test_probe_permission_failure_is_not_group_absence(self):
        waits = []
        process = SimpleNamespace(pid=123, wait=lambda timeout: waits.append(timeout))
        with patch.object(run_pilot.os, "killpg", side_effect=[None, PermissionError("synthetic probe EPERM")]):
            with self.assertRaisesRegex(RuntimeError, "termination unverified.*probe EPERM"):
                run_pilot.terminate_group(process)
        self.assertEqual(waits, [run_pilot.TERMINATION_GRACE_SECONDS] * 2)

    def test_primary_failure_survives_cleanup_failure_and_stops_campaign(self):
        with tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
            root = Path(directory)
            (root / "A").mkdir()
            (root / "A/probe.md").write_text("synthetic guidance")
            args = SimpleNamespace(output=root, guidance=root, runtime="claude", model="fixture", effort="fixture", fallback=None)
            case = {"id": "probe", "kind": "audit", "prompt": "synthetic"}
            class FailedInput(io.StringIO):
                def write(self, _text):
                    raise OSError("synthetic primary error")
            process = SimpleNamespace(stdin=FailedInput())
            with patch.object(run_pilot.subprocess, "Popen", return_value=process), patch.object(run_pilot, "terminate_group", side_effect=RuntimeError("synthetic cleanup error")):
                with self.assertRaisesRegex(RuntimeError, "primary error.*cleanup error") as caught:
                    run_pilot.run_one(args, case, "A", 1)
            self.assertIsInstance(caught.exception.__cause__, OSError)
            self.assertTrue(run_pilot.STOP.is_set())

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
