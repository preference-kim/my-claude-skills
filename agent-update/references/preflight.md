## Resolve the repositories

Resolve paths from this skill rather than assuming where dotfiles was cloned.
Private-only synchronization uses steps 1–3; layout validation, installation and
upstream work in the remaining steps apply to agent-file refresh or installation:

1. Resolve this skill's real path and run `git rev-parse --show-toplevel` from it to find the skills repository.
2. Run `git rev-parse --show-toplevel` from the skills repository's parent to find the dotfiles repository.
3. Use `<dotfiles>/AGENTS.md` as the canonical instruction file and `<dotfiles>/skills` as the skills repository.
4. Determine the current host's layout mode: read `mode:` from `<dotfiles>/agent-file-sync.local.yaml` if it exists and require `host-global` or `moreh-dev`. This file is host-local and gitignored, never committed, so it never reflects another host's setting. If it is absent or the mode is invalid, the host has no usable configuration; do not guess or fall back to a default, and do not create or edit it without being asked (point to `agent-file-sync.example.yaml` instead).
5. When the mode is `moreh-dev`, read the required non-empty `moreh_dev_root` from the same file. Use an absolute path as written; resolve a relative path from the dotfiles root. Canonicalize the result, require the directory to exist, and require `git -C <candidate> rev-parse --show-toplevel` to resolve to that exact directory. Do not expand shell expressions, search for, create, or clone an alternate checkout when the configured target is absent or invalid; report that project synchronization could not run. Continue the user-scope skill installation for a valid mode, but do not write the successful-sync stamp. A project-root failure must not block the independent user-scope installation.
6. Read [upstream.md](upstream.md) before comparing or updating upstream content.

## Choose the mode

- **Daily refresh:** When the canonical AGENTS requests the session-start refresh, skip public repository and CLI work if `${XDG_STATE_HOME:-$HOME/.local/state}/agent-update/last-successful-sync` contains today's local date. Still clean completed workspace artifacts, verify and repair the current host's configured entry points and complete skill manifest, and run approved SSH synchronization. The public date stamp never skips the private SSH fetch and drift check. Otherwise run the full refresh.
- **Forced refresh:** For `/agent-update`, `$agent-update`, or a direct agent refresh request, ignore the date stamp and run the full agent-file and CLI refresh plus approved SSH synchronization. This does not request source review, server bootstrap, hosts-file writes or HF or GitHub token synchronization.
- **Requested edit:** When the user supplies update text, refresh first, including approved SSH synchronization, then apply that request to the canonical AGENTS or shared skills before validation and publication.
- **Link repair:** When asked to install or repair shared agent files, run the current host's symlink checks even if today's refresh already succeeded.
- **Private synchronization only:** For an explicit request to set up, synchronize or repair private server configuration, or set up, repair or synchronize enrolled credentials, resolve only the canonical repository paths in steps 1–3 above and read `private-sync.md`. Run only its requested payloads and targets under its writer-lock and approval rules. This mode is not an agent refresh: skip public agent-file/CLI updates, cleanup, installation/manifest verification and upstream reconciliation, and leave the daily refresh stamp unchanged. Run those stages only if the user also requests an agent refresh.

## Lock and preflight

Use `${XDG_STATE_HOME:-$HOME/.local/state}/agent-update/lock` as an atomic directory lock. Record the current hostname and PID, remove the lock on exit, and reclaim it only when its recorded process is no longer alive on the same host.

Before changing tracked files:

1. Inspect `git status --short --branch` in both repositories.
2. Require `main`, no unrelated tracked or untracked changes, and a fast-forward relationship with each `origin/main`.
3. Fetch both origins. Pull the dotfiles repository with `--ff-only`, synchronize submodule URLs recursively, initialize and update submodules recursively, switch the skills repository to `main`, and pull it with `--ff-only`.
4. If AGENTS.md or this skill changed during the pull, re-read them and read each later stage reference from the updated checkout. The updated text replaces the version loaded at session start for the remaining stages; a difference between the two is not a question for the user.
5. Stop without stashing, rebasing, resetting, or force-pushing when these conditions are not satisfied.

If a requested edit belongs to an existing user-owned nested skill repository,
verify that repository's ownership, clean tree, and fast-forward relationship to
its `origin/main` before editing. Switch it to `main` and fast-forward through
its existing origin; do not leave new work on a detached submodule HEAD. Leave
unrelated or vendor-owned nested repositories at their recorded commits. Publish
the changed child before either parent, as required by publication.md.
