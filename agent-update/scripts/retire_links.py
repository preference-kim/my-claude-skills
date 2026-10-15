#!/usr/bin/env python3
"""Plan removal of exact managed reference/duplicate links; preserve overrides."""

import argparse
import configparser
import json
import os
from pathlib import Path
import subprocess


def read_scopes(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate installation key: " + key)
            result[key] = value
        return result
    scopes = json.loads(path.read_text(), object_pairs_hook=unique)
    if not isinstance(scopes, dict) or any(value not in {"user", "moreh-dev", "reference"} for value in scopes.values()):
        raise ValueError("invalid installation scope")
    return scopes


def tracked(project, path):
    result = subprocess.run(
        ["git", "-C", str(project), "ls-files", "--error-unmatch", "--", str(path.relative_to(project))],
        capture_output=True, text=True,
    )
    if result.returncode not in (0, 1):
        raise ValueError("cannot establish project tracking state")
    return result.returncode == 0


def candidates(dotfiles, user_root, project, mode, references):
    """Only current canonical links qualify. Prior installations require inspection."""
    skills = dotfiles / "skills"
    roots = [user_root / ".agents/skills", user_root / ".codex/skills", user_root / ".claude/skills"]
    if project:
        roots += [project / ".agents/skills", project / ".codex/skills", project / ".claude/skills"]
    result = []
    for root in roots:
        for name, subpath in references.items():
            result.append((root / name, skills / name / subpath, "reference discovery"))
    if mode == "moreh-dev":
        for runtime, filename in [(".codex", "AGENTS.md"), (".claude", "CLAUDE.md")]:
            # The retained project link must resolve correctly before removing its duplicate.
            retained = project / filename
            if retained.is_symlink() and retained.resolve() == (dotfiles / filename).resolve():
                result.append((user_root / runtime / filename, dotfiles / filename, "duplicate instructions"))
    return result


def plan(dotfiles, user_root, project, mode, references):
    actions = []
    for path, source, reason in candidates(dotfiles, user_root, project, mode, references):
        if not path.exists() and not path.is_symlink():
            continue
        project_path = project and path.is_relative_to(project)
        status = "preserve override"
        anchor = project if project_path else user_root
        parents = [parent for parent in path.parents if parent != anchor and parent.is_relative_to(anchor)]
        if any(parent.is_symlink() for parent in parents):
            status = "preserve discovery-root override"
        elif project_path and tracked(project, path):
            status = "preserve tracked path"
        elif path.is_symlink():
            target = path.resolve()
            canonical = source.resolve()
            if target == canonical:
                status = "remove managed link"
        actions.append({"path": str(path), "status": status, "reason": reason,
                        "anchor": str(anchor),
                        "link": os.readlink(path) if path.is_symlink() else None})
    return actions


def apply(actions):
    for action in actions:
        if action["status"] == "remove managed link":
            path = Path(action["path"])
            anchor = Path(action["anchor"])
            parent_changed = any(parent.is_symlink() for parent in path.parents
                                 if parent != anchor and parent.is_relative_to(anchor))
            if parent_changed or not path.is_symlink() or os.readlink(path) != action["link"]:
                raise ValueError("link changed after planning: " + str(path))
            path.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dotfiles", type=Path, required=True)
    parser.add_argument("--user-root", type=Path, default=Path.home())
    parser.add_argument("--mode", choices=["host-global", "moreh-dev"], required=True)
    parser.add_argument("--project", type=Path)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    dotfiles = args.dotfiles.resolve()
    project = args.project.resolve() if args.project else None
    if args.mode == "moreh-dev" and project is None:
        parser.error("moreh-dev requires the validated --project")
    if project:
        actual = subprocess.check_output(["git", "-C", str(project), "rev-parse", "--show-toplevel"], text=True).strip()
        if Path(actual).resolve() != project:
            parser.error("project must be an exact repository root")
    scopes = read_scopes(dotfiles / "skills/.installation-policy.json")
    modules = configparser.ConfigParser(interpolation=None)
    modules.read(dotfiles / "skills/.gitmodules")
    subpaths = {modules[s]["path"]: modules[s].get("skill-path", ".") for s in modules.sections()}
    refs = {name: subpaths.get(name, ".") for name, scope in scopes.items() if scope == "reference"}
    if any(not name or Path(name).name != name or name in {".", ".."} for name in refs):
        parser.error("invalid source key")
    if any(Path(subpath).is_absolute() or ".." in Path(subpath).parts for subpath in refs.values()):
        parser.error("invalid skill-path")
    actions = plan(dotfiles, args.user_root.resolve(), project, args.mode, refs)
    if args.apply:
        apply(actions)
    print(json.dumps({"applied": args.apply, "actions": actions}, indent=2))


if __name__ == "__main__":
    main()
