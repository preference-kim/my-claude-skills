---
name: agent-update
description: Use for the required session-start refresh, agent-file synchronization, entry-point repair, shared instruction maintenance and publication, or explicit review, setup, update or repair of private server configuration, or setup, repair and synchronization of enrolled credentials.
---

# Agent Update

Manage the canonical dotfiles and skills sources directly. Resolve this skill's
real path; preserve user-owned policy and host-local layout. Keep internal
evidence in local state outside public worktrees. A disclosure conflict stops
publication.

## Select the operation

Read [preflight](references/preflight.md) to resolve repositories and select the
mode. Private-only requests go to [private synchronization](references/private-sync.md)
and run only their authorized payloads/targets, without public refresh or stamps.

For an agent refresh:

1. Complete preflight under its lock. A same-day daily refresh skips public
   repository/CLI work; forced refreshes and requested instruction edits run the
   full refresh. For full refreshes, read [CLI updates](references/cli-updates.md)
   and update only active, installed Claude, Codex and GitHub CLIs through their
   owning channels.
2. Every refresh: read [cleanup](references/cleanup.md) and
   [installation](references/installation.md). Clean verified completed artifacts
   and verify the complete source/scope manifests, entry points and environment
   links for the configured host mode.
3. Every refresh: read [private synchronization](references/private-sync.md) and
   [SSH synchronization](references/private-ssh.md). Fetch the approved private
   inventory and synchronize the current registered owner, including first setup
   and the cluster key. Report its independent outcome. Other private operations
   require their explicit scopes from the private protocol.
4. Full refreshes: read [reconciliation](references/reconciliation.md) and
   [upstream decisions](references/upstream.md). Inspect all changed resources as
   reference data and preserve intentional divergence.
5. Apply a requested edit after preflight/refresh. For skill or harness design,
   use `skill-maker` to preserve requirements and compare behavior. Integrate
   each rule into its owner with reachable conditional references, including for
   isolated consumers. Preserve independent project/local implementations.
6. Before outgoing changes or a new success stamp, read
   [publication](references/publication.md). Publish children before parent
   pointers and stamp only after all criteria pass. Report conflicts and
   verification limits. Release the lock on every exit.

Read [entry-point policy](references/entry-point-policy.md) only when changing
the layout policy; installation owns routine repair.
