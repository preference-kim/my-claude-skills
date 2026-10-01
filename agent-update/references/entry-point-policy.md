## Agent file sync

This file is the canonical shared guidance for Codex and Claude. The concrete entry-point layout is a per-host choice, not fixed in this document: it is recorded in `agent-file-sync.local.yaml` at the dotfiles root, a host-local file that is gitignored and never committed, based on the template in the tracked `agent-file-sync.example.yaml`. In `moreh-dev` mode, the same file records `moreh_dev_root`, the host-specific Git checkout root that receives the entry points. Because the file never syncs through git, no agent-update run on any host can read, set, or overwrite another host's mode or target; each host's choice exists only on that host, made there directly.

Both modes install `user` skills from the canonical
`skills/.installation-policy.json` at `~/.agents/skills/<name>` for Codex and
`~/.claude/skills/<name>` for Claude. Keep real roots and individual links.
Publication approval and installation scope are separate requirements.

- `host-global`: keep instruction links at `~/.codex/AGENTS.md` and
  `~/.claude/CLAUDE.md`. Exclude `moreh-dev` skills from global installation.
- `moreh-dev`: keep instruction links at the configured checkout's
  `AGENTS.md`/`CLAUDE.md`. Install only `moreh-dev` skills in its
  `.agents/skills/<name>` and `.claude/skills/<name>` directories. User skills
  remain available through their global installation; do not duplicate them
  in the checkout or add host-global instructions.

An absent or invalid mode blocks installation. An invalid `moreh_dev_root`
blocks project synchronization while user-scope installation continues for a
valid mode. Never infer a mode or search for a checkout; withhold the successful
refresh stamp when required project installation is blocked. The
[installation rules](installation.md) own conflict handling, canonical reference
resolution, legacy migration, and complete manifest verification.

At the start of the first user task in each new session, use the `agent-update` skill for its daily refresh. The skill skips network and repository work after a successful refresh on the same local calendar day, but always verifies and repairs the current host's configured entry points and skill links. If it pulls or reconciles changed instructions, re-read the updated AGENTS.md and skill files before continuing.

Each full refresh also keeps installed Claude Code CLI, Codex CLI, and GitHub CLI commands on the latest release available through their verified existing installation channels. It updates only the active installation and its named package, never installs a missing command or performs a package-manager-wide upgrade, and withholds the successful-sync stamp when a command is known to be outdated but cannot be updated or verified.

Use `/agent-update` or `$agent-update` to force a refresh, edit shared agent instructions or skills, repair the current host's links, publish agent-file changes, or set this host's mode and target in `agent-file-sync.local.yaml`. Synchronization must compare the local design with `csehydrogen/.files` semantically; never overwrite intentional local policy with a wholesale upstream copy.
