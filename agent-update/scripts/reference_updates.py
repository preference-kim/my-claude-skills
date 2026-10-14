#!/usr/bin/env python3
"""Report changes to pinned reference sources without updating any Git checkout."""

import argparse
import configparser
import fcntl
import json
import os
from pathlib import Path
import re
import subprocess
from urllib.parse import quote


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate key: " + key)
        result[key] = value
    return result


def read_json(path):
    return json.loads(path.read_text(), object_pairs_hook=unique_object)


def registered_references(root):
    scopes = read_json(root / ".installation-policy.json")
    if not isinstance(scopes, dict):
        raise ValueError("installation policy must be an object")
    if any(scope not in {"user", "moreh-dev", "reference"} for scope in scopes.values()):
        raise ValueError("unknown installation scope")
    allowed = read_json(root / ".publication-policy.json")["paths"]
    modules = configparser.ConfigParser(interpolation=None)
    modules.read(root / ".gitmodules")
    by_path = {modules[s]["path"]: modules[s] for s in modules.sections()}
    result = []
    for name, scope in scopes.items():
        if scope != "reference":
            continue
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            raise ValueError("invalid reference name")
        if name not in allowed or name not in by_path:
            raise ValueError("reference is not an approved gitlink: " + name)
        module = by_path[name]
        match = re.fullmatch(r"(?:https://github\.com/|git@github\.com:)([\w.-]+/[\w.-]+?)(?:\.git)?", module["url"])
        if not match:
            raise ValueError("unsupported reference remote: " + name)
        record = subprocess.check_output(
            ["git", "-C", str(root), "ls-tree", "HEAD", "--", name], text=True
        ).split()
        if len(record) != 4 or record[:2] != ["160000", "commit"] or record[3] != name:
            raise ValueError("reference has no committed gitlink: " + name)
        result.append({"name": name, "repo": match[1], "branch": module.get("branch"), "pin": record[2]})
    return result


def github(endpoint):
    # Only public repository metadata is requested; never print CLI stderr/tokens.
    result = subprocess.run(["gh", "api", endpoint], capture_output=True, text=True, timeout=45)
    if result.returncode:
        raise ValueError("upstream lookup failed")
    return json.loads(result.stdout)


def inspect_reference(ref, prior, api=github):
    """Return a notice and cursor; None means unchanged or fewer than five commits."""
    branch = ref["branch"] or api("repos/" + ref["repo"])["default_branch"]
    head = api("repos/" + ref["repo"] + "/commits/" + quote(branch, safe=""))["sha"]
    if not re.fullmatch(r"[0-9a-f]{40}", head):
        raise ValueError("invalid upstream revision")
    identity = {"repo": ref["repo"], "branch": branch, "pin": ref["pin"]}
    cursor = prior if prior and prior.get("identity") == identity else {}
    baseline = cursor.get("head", ref["pin"])
    if head == baseline:
        return None, {key: value for key, value in cursor.items() if key != "diverged"}
    comparison = api("repos/" + ref["repo"] + "/compare/" + baseline + "..." + head)
    status = comparison["status"]
    if status == "identical":
        return None, {key: value for key, value in cursor.items() if key != "diverged"}
    if status == "ahead":
        count = comparison["ahead_by"]
        if not isinstance(count, int) or count < 0:
            raise ValueError("invalid upstream commit count")
        if count < 5:
            return None, {key: value for key, value in cursor.items() if key != "diverged"}
        message = f"{ref['name']}: {count} additional upstream commits; consider a separate reference review."
    elif status in {"behind", "diverged"}:
        if cursor.get("diverged"):
            return None, cursor
        message = f"{ref['name']}: upstream history no longer advances the recorded revision; inspect separately."
        return message, {"identity": identity, "head": baseline, "diverged": True}
    else:
        raise ValueError("unknown comparison status")
    return message, {"identity": identity, "head": head}


def check(root, state_dir, api=github):
    state_dir.mkdir(parents=True, exist_ok=True)
    with (state_dir / "reference-notices.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        path = state_dir / "reference-notices.json"
        state = read_json(path) if path.exists() else {}
        if not isinstance(state, dict) or any(not isinstance(value, dict) for value in state.values()):
            raise ValueError("invalid reference notice state")
        messages = []
        for ref in registered_references(root):
            try:
                notice, cursor = inspect_reference(ref, state.get(ref["name"]), api)
            except (KeyError, ValueError, OSError, subprocess.SubprocessError, TypeError):
                # Preserve the last successful cursor. One failure notice per outage.
                cursor = state.get(ref["name"], {}).copy()
                if not cursor.get("lookup_failed"):
                    messages.append(ref["name"] + ": reference update check unavailable; pin unchanged.")
                cursor["lookup_failed"] = True
            else:
                cursor = cursor.copy()
                cursor.pop("lookup_failed", None)
                if notice:
                    messages.append(notice)
            state[ref["name"]] = cursor
        serialized = json.dumps(state, indent=2, sort_keys=True) + "\n"
        if not path.exists() or path.read_text() != serialized:
            pending = path.with_suffix(".pending")
            pending.write_text(serialized)
            pending.replace(path)
        return messages


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-root", type=Path, required=True)
    parser.add_argument("--state-dir", type=Path, default=Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local/state")) / "agent-update")
    args = parser.parse_args()
    try:
        for message in check(args.skills_root.resolve(), args.state_dir):
            print(message)
    except (KeyError, ValueError, OSError, subprocess.SubprocessError, TypeError, configparser.Error):
        print("Reference update check unavailable: inspect registry or local notice state; pins unchanged.")
    # Advisory checks never block the independent installation/refresh workflow.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
