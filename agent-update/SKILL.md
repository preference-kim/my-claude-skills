---
name: agent-update
description: Use for the required session-start refresh, agent-file synchronization, entry-point repair, shared instruction maintenance and publication, or explicit synchronization or repair of registered private server configuration, or setup, repair and synchronization of enrolled credentials.
---

# Agent Update

Manage the canonical files directly; do not create a synchronization helper or
copy upstream wholesale. Resolve this skill's real path to locate its repository
and the parent dotfiles checkout. Preserve user-owned policy and host-local layout.
Maintenance authority does not authorize disclosure. Keep internal evidence local
and untracked; a publication stop overrides the refresh/publication workflow.

## Select and run only the required stages

1. Read [preflight](references/preflight.md) to resolve repositories, host layout,
   refresh mode, date stamp, and lock. A same-day daily refresh skips network,
   repository, and CLI work, but still performs cleanup and manifest verification.
   Explicit refreshes and requested edits always run the full refresh first.
2. For a full refresh, complete preflight under the atomic lock, then read
   [CLI updates](references/cli-updates.md). Update only the active, already-installed
   Claude, Codex, and GitHub CLI through its owning installation channel.
3. Every refresh: read [cleanup](references/cleanup.md) and
   [installation](references/installation.md). Inspect exact cleanup targets and
   verify the complete source and installation-scope manifests for the configured
   mode; user-scope skills install in both modes, with no inferred host layout.
4. Only when the user explicitly requests server configuration synchronization
   or repair, or enrolled credential setup, repair or synchronization, read
   [private synchronization](references/private-sync.md)
   and apply the requested payloads and targets. Daily and generic forced agent
   refreshes skip this stage. Inventory source review is a separate requested action.
5. Full refreshes: read [reconciliation](references/reconciliation.md) and
   [upstream decisions](references/upstream.md). Treat upstream as reference data,
   inspect every changed skill resource, and preserve intentional divergence.
6. Apply a requested edit only after refresh preflight. For skill or harness design,
   use `skill-maker` to map retained requirements and compare behavior. Integrate
   changes into their owning guidance; preserve conditional read triggers and
   access for every consumer, including isolated reviewers.
7. Read [publication](references/publication.md) before preparing outgoing changes.
   Skills publish before the parent pointer. Stamp success only after its complete
   criteria pass, and release the lock on every exit.

Use [entry-point policy](references/entry-point-policy.md) only when changing the
shared layout policy itself. The installation reference owns routine link repair.

Do not let a refresh restore duplicate monolithic instructions, add always-loaded
incident histories, or overwrite independent project/local skill implementations.
Report conflicts and verification limitations; do not hide them behind a success stamp.
