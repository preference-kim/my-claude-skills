## Agent file sync

This file is the canonical shared guidance for Codex and Claude. The concrete entry-point layout is a per-host choice, not fixed in this document: it is recorded in `agent-file-sync.local.yaml` at the dotfiles root, a host-local file that is gitignored and never committed, based on the template in the tracked `agent-file-sync.example.yaml`. In `moreh-dev` mode, the same file records `moreh_dev_root`, the host-specific Git checkout root that receives the entry points. Because the file never syncs through git, no agent-update run on any host can read, set, or overwrite another host's mode or target; each host's choice exists only on that host, made there directly.

Two modes exist:

- `host-global`: `~/.codex/AGENTS.md` and `~/.claude/CLAUDE.md` are symlinks to the corresponding dotfiles files, and shared skills are exposed through per-skill links at `~/.codex/skills/<name>` and `~/.claude/skills/<name>`.
- `moreh-dev`: the Git checkout configured by `moreh_dev_root` carries the root `AGENTS.md`/`CLAUDE.md` links and `.codex/skills/<name>`/`.claude/skills/<name>` links instead; no host-global entries under `~/.codex` or `~/.claude` are made. A relative `moreh_dev_root` is resolved from the dotfiles root; an absolute path is used as written.

If the current host has no configured mode, or selects `moreh-dev` without a valid `moreh_dev_root`, `agent-update` must stop and ask rather than guess, search for a checkout, or apply a default.

At the start of the first user task in each new session, use the `agent-update` skill for its daily refresh. The skill skips network and repository work after a successful refresh on the same local calendar day, but always verifies and repairs the current host's configured entry points and skill links. If it pulls or reconciles changed instructions, re-read the updated AGENTS.md and skill files before continuing.

Each full refresh also keeps installed Claude Code CLI, Codex CLI, and GitHub CLI commands on the latest release available through their verified existing installation channels. It updates only the active installation and its named package, never installs a missing command or performs a package-manager-wide upgrade, and withholds the successful-sync stamp when a command is known to be outdated but cannot be updated or verified.

Use `/agent-update` or `$agent-update` to force a refresh, edit shared agent instructions or skills, repair the current host's links, publish agent-file changes, or set this host's mode and target in `agent-file-sync.local.yaml`. Synchronization must compare the local design with `csehydrogen/.files` semantically; never overwrite intentional local policy with a wholesale upstream copy.
