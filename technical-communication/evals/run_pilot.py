#!/usr/bin/env python3
"""Run fresh, explicitly supplied-guidance cases; never infer installed discovery."""

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import random
import signal
import subprocess
import threading
import time


CODEX_SETTINGS = [
    "project_doc_max_bytes=0", "skills.include_instructions=false",
    "skills.bundled.enabled=false", "features.apps=false", "features.plugins=false",
    "features.memories=false", "agents.enabled=false", "features.multi_agent_v2=false",
    'approval_policy="never"',
]
COMMON = """This is a synthetic engineering evaluation. All source evidence is supplied.
Act on the task using the supplied guidance. Do not invent sources or execution.
For document cases produce the author draft only; independent review and publication
are outside your authority. Do not delegate or consult external resources.
Referenced resources not supplied here are outside this exercise. Do not treat
fictional source records as measurements of a real system.

The evaluation restrictions above apply to this model invocation. In a document
about another task or agent, TASK defines that task's authority and constraints.
Preserve those constraints; do not transfer an evaluation restriction to the
document's recipient unless TASK also assigns it to that recipient.
"""
STOP = threading.Event()
LAUNCH_LOCK = threading.Lock()
RUN_TIMEOUT_SECONDS = 600
TERMINATION_GRACE_SECONDS = 5


def quota_stop_reason(event):
    if not isinstance(event, dict):
        return None
    if event.get("type") == "rate_limit_event":
        info = event.get("rate_limit_info", {})
        if not isinstance(info, dict):
            return None
        if info.get("isUsingOverage") or info.get("overageInUse"):
            return "provider reports overage usage"
        if info.get("status") == "rejected" and info.get("rateLimitType") in {"five_hour", "seven_day"}:
            return "provider reports exhausted account-wide quota"
        if info.get("status") == "rejected" and info.get("rateLimitType") == "overage":
            return "provider reports exhausted overage quota"
        return None
    if event.get("type") == "error":
        message = event.get("message")
    elif event.get("type") == "turn.failed" and isinstance(event.get("error"), dict):
        message = event["error"].get("message")
    else:
        return None
    # Codex 0.162.1 JSONL carries messages, not the structured quota subtype.
    # Match its account-limit messages, not transient capacity/rate-limit errors
    # or the distinct "usage limit for <model>" message.
    # https://github.com/openai/codex/blob/092d3acd6bec3e3a14bdc7e7a2810ab628ab759d/codex-rs/protocol/src/error.rs
    if isinstance(message, str) and message.replace("’", "'").casefold().startswith((
        "you've hit your usage limit.",
        "quota exceeded. check your plan and billing details.",
        "your workspace is out of credits.",
        "you hit your spend cap set in your workspace.",
        "you hit your spend cap set by the owner of your workspace.",
        "to use codex with your chatgpt plan, upgrade to plus:",
    )):
        return "provider reports exhausted account quota or unavailable plan access"
    return None


def stop_campaign():
    # Serialize the stop transition with launches, including work already prepared.
    with LAUNCH_LOCK:
        STOP.set()


def terminate_group(process):
    failure = None
    group_gone = False
    try:
        for sig in (signal.SIGTERM, signal.SIGKILL):
            process.poll()
            try:
                os.killpg(process.pid, sig)
            except ProcessLookupError:
                group_gone = True
                break
            except PermissionError as error:
                # On macOS an exited, unreaped group can return EPERM. Reap
                # and retry within the deadline; EPERM alone never proves absence.
                failure = error
            deadline = time.monotonic() + TERMINATION_GRACE_SECONDS
            try:
                process.wait(timeout=TERMINATION_GRACE_SECONDS)
            except subprocess.TimeoutExpired:
                pass
            while True:
                # Reap the leader before probing survivors when possible.
                try:
                    os.killpg(process.pid, 0)
                except ProcessLookupError:
                    group_gone = True
                    break
                except PermissionError as error:
                    failure = error
                if time.monotonic() >= deadline:
                    break
                time.sleep(0.05)
            if group_gone:
                break
    except OSError as error:
        failure = error
    finally:
        # Signaling/probing may fail. Still make an independent, bounded reap.
        try:
            process.wait(timeout=TERMINATION_GRACE_SECONDS)
        except (OSError, subprocess.TimeoutExpired) as error:
            detail = "leader reaping unverified: " + str(error)
            if failure is not None:
                detail = str(failure) + "; " + detail
            raise RuntimeError("process-group termination unverified: " + detail) from failure
    if failure is not None and not group_gone:
        raise RuntimeError("process-group termination unverified: " + str(failure)) from failure
    if not group_gone:
        raise RuntimeError("process-group termination unverified: group still present")


def codex_isolation(root):
    cmd = ["codex"]
    for value in CODEX_SETTINGS:
        cmd += ["-c", value]
    result = subprocess.run(cmd + ["debug", "prompt-input", "Isolation probe; do not execute a task."], cwd=root, capture_output=True, text=True, timeout=60)
    (root / "isolation.json").write_text(result.stdout)
    (root / "isolation.stderr").write_text(result.stderr)
    if result.returncode:
        return "Codex prompt inspection unavailable"
    # Global instructions are not controlled by project_doc_max_bytes in all versions.
    if "AGENTS.md instructions" in result.stdout or "<skills_instructions>" in result.stdout:
        return "Codex still injects ambient instructions; controlled comparison blocked"
    # prompt-input omits the tool catalog. A read-only sandbox still exposes
    # tools, so a clean prompt is insufficient to authorize an actor run.
    return "Codex per-case tool boundaries are unverified; controlled comparison blocked"


def run_one(args, case, variant, repeat):
    if STOP.is_set():
        return {"case": case["id"], "variant": variant, "repeat": repeat, "status": "not_started_campaign_stop"}
    directory = args.output / f"{variant}-{case['id']}-{repeat}"
    directory.mkdir()
    workspace = directory / "workspace"
    workspace.mkdir()
    for name, content in case.get("files", {}).items():
        (workspace / name).write_text(content)
    guidance = (args.guidance / variant / (case["id"] + ".md")).read_text()
    prompt = COMMON + "\nSUPPLIED GUIDANCE\n" + guidance + "\nTASK\n" + case["prompt"]
    if case["kind"] == "repair":
        prompt += "\nExecution environment: Bash permits exactly `python3 verify_example.py`. Use that command without a path prefix, cd, or appended shell commands. The tool reports exit status separately."
    (directory / "prompt.txt").write_text(prompt)
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    repair = case["kind"] == "repair"
    if args.runtime == "claude":
        for name in ("CLAUDE_CODE_OAUTH_TOKEN", "ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN"):
            env.pop(name, None)
        cmd = ["claude", "--safe-mode", "--restricted", "--strict-mcp-config", "--disable-slash-commands",
               "--no-session-persistence", "--print", "--verbose", "--output-format", "stream-json",
               "--model", args.model, "--effort", args.effort, "--permission-mode", "dontAsk",
               "--permission-prompts", "none", "--tools", "Read,Edit,Bash" if repair else ""]
        if args.fallback:
            cmd += ["--fallback-model", args.fallback]
        if repair:
            cmd += ["--allowedTools", "Read", "Edit", "Bash(python3 verify_example.py)"]
    else:
        cmd = ["codex", "exec", "--ignore-user-config", "--ignore-rules", "--strict-config",
               "--ephemeral", "--skip-git-repo-check", "--json", "--model", args.model,
               "--sandbox", "workspace-write" if repair else "read-only"]
        for value in CODEX_SETTINGS + ["model_reasoning_effort=" + json.dumps(args.effort)]:
            cmd += ["-c", value]
        cmd += ["-"]
    start = time.monotonic()
    stop_reason = None
    # A file avoids blocking the worker on a pipe write before it can monitor STOP.
    with (directory / "prompt.txt").open() as stdin, (directory / "events.jsonl").open("w") as output, (directory / "stderr.txt").open("w") as stderr:
        with LAUNCH_LOCK:
            if STOP.is_set():
                return {"case": case["id"], "variant": variant, "repeat": repeat, "status": "not_started_campaign_stop"}
            process = subprocess.Popen(cmd, stdin=stdin, text=True, stdout=output, stderr=stderr,
                                       cwd=workspace, env=env, start_new_session=True)
        try:
            with (directory / "events.jsonl").open() as tail:
                pending = ""
                while True:
                    pending += tail.read()
                    lines = pending.split("\n")
                    pending = lines.pop()
                    for line in lines:
                        try:
                            reason = quota_stop_reason(json.loads(line))
                        except (json.JSONDecodeError, AttributeError):
                            continue
                        if reason:
                            stop_reason = reason
                            stop_campaign()
                    if STOP.is_set():
                        terminate_group(process)
                        status = "quota_stopped" if stop_reason else "campaign_stopped"
                        break
                    if process.poll() is not None:
                        status = "completed" if process.returncode == 0 else "process_failed"
                        break
                    if time.monotonic() - start >= RUN_TIMEOUT_SECONDS:
                        terminate_group(process)
                        status = "timeout"
                        break
                    time.sleep(0.2)
            code = process.returncode
        except BaseException as failure:
            stop_campaign()
            try:
                terminate_group(process)
            except Exception as cleanup:
                raise RuntimeError(f"pilot failure: {failure}; cleanup failure: {cleanup}") from failure
            raise
    events = []
    for line in (directory / "events.jsonl").read_text().splitlines():
        try:
            event = json.loads(line)
            if isinstance(event, dict):
                events.append(event)
        except json.JSONDecodeError:
            continue
    response = ""
    model_usage = {}
    initialization = None
    for event in events:
        # Include output written between the last tail read and process exit.
        reason = quota_stop_reason(event)
        if reason:
            stop_reason = reason
            stop_campaign()
            terminate_group(process)
            status = "quota_stopped"
        if event.get("type") == "system" and event.get("subtype") == "init":
            initialization = event
        if event.get("type") == "result":
            response = event.get("result", "")
            model_usage = event.get("modelUsage", {})
            if event.get("is_error") and status not in {"quota_stopped", "timeout"}:
                status = "model_failed"
        if event.get("type") == "item.completed" and event.get("item", {}).get("type") == "agent_message":
            response = event["item"]["text"]
    # Safe mode retains provider-built-in plugins, including security policy.
    # They are runtime controls, not installed user guidance, and stay enabled.
    isolation_verified = args.runtime != "claude" or bool(initialization is not None and not initialization.get("skills") and not initialization.get("mcp_servers") and all(plugin.get("path") == "builtin" for plugin in initialization.get("plugins", [])))
    if not isolation_verified and status == "completed":
        status = "isolation_unverified"
    (directory / "response.md").write_text(response)
    record = {"case": case["id"], "variant": variant, "repeat": repeat, "runtime": args.runtime,
              "requested_model": args.model, "effort": args.effort, "model_usage": model_usage,
              "status": status, "exit_code": code, "elapsed_seconds": round(time.monotonic() - start, 2),
              "stop_reason": stop_reason, "isolation_verified": isolation_verified,
              "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(), "response_words": len(response.split())}
    (directory / "record.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({key: record[key] for key in ("case", "variant", "repeat", "status", "elapsed_seconds")}), flush=True)
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=Path(__file__).with_name("cases.json"))
    parser.add_argument("--guidance", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--runtime", choices=["codex", "claude"], required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--effort", required=True)
    parser.add_argument("--fallback")
    parser.add_argument("--partition", choices=["development", "holdout"], required=True)
    parser.add_argument("--case-id", help="Run one case across its full variant/repeat matrix; record reruns separately")
    args = parser.parse_args()
    STOP.clear()
    args.output.mkdir(parents=True, exist_ok=False)
    args.output = args.output.resolve()
    args.guidance = args.guidance.resolve()
    cases = [case for case in json.loads(args.cases.read_text()) if case["partition"] == args.partition]
    if args.case_id:
        cases = [case for case in cases if case["id"] == args.case_id]
        if not cases:
            parser.error("case-id is absent from the selected partition")
    if args.runtime == "codex":
        reason = codex_isolation(args.output)
        if reason:
            (args.output / "blocked.json").write_text(json.dumps({"reason": reason, "generations": 0}, indent=2) + "\n")
            print(reason, flush=True)
            return 2
    variants = ["C"] if args.partition == "holdout" else ["A", "B", "C"]
    jobs = [(case, variant, repeat) for case in cases for variant in variants for repeat in (1, 2)]
    random.Random(20261014).shuffle(jobs)
    def terminate_controller(signum, _frame):
        raise SystemExit(128 + signum)
    previous_term = signal.signal(signal.SIGTERM, terminate_controller)
    previous_int = signal.signal(signal.SIGINT, terminate_controller)
    failure = None
    try:
        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = []
            try:
                for job in jobs:
                    futures.append(pool.submit(run_one, args, *job))
                records = [future.result() for future in futures]
            except BaseException as error:
                # Children have separate sessions. Stop launches before waiting
                # for workers, and do not interrupt their bounded cleanup again.
                signal.signal(signal.SIGINT, signal.SIG_IGN)
                signal.signal(signal.SIGTERM, signal.SIG_IGN)
                stop_campaign()
                for future in futures:
                    future.cancel()
                failure = error
        if failure is not None:
            worker_errors = [future.exception() for future in futures if not future.cancelled()]
            other_errors = [error for error in worker_errors if error is not None and error is not failure]
            if other_errors:
                details = "; ".join(str(error) for error in other_errors)
                raise RuntimeError(f"controller failure: {type(failure).__name__}: {failure}; worker failures: {details}") from failure
            raise failure
    finally:
        signal.signal(signal.SIGTERM, previous_term)
        signal.signal(signal.SIGINT, previous_int)
    (args.output / "summary.json").write_text(json.dumps(records, indent=2) + "\n")
    if STOP.is_set():
        print("Campaign stopped at a quota/overage signal; do not launch more model runs.", flush=True)
        return 3
    return 0 if all(record["status"] == "completed" for record in records) else 1


if __name__ == "__main__":
    raise SystemExit(main())
