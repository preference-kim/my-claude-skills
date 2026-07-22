# Upstream Agent Guidance

## Reviewed source

- Repository: `https://github.com/csehydrogen/.files.git`
- Branch: `master`
- Reviewed commit: `5739bc5fe0de6f7fc0b5bab55b664fd57facbcd7`
- Instruction path: `AGENTS.md`
- Skill path: `skills/agent-update/SKILL.md`

Advance the reviewed commit only after both paths at the new commit have been inspected and every applicable change has been reconciled or consciously covered by an intentional divergence.

## Local design

- Keep `AGENTS.md` at the dotfiles root as the canonical instruction file.
- Keep the user-owned stable working principles at the top of `AGENTS.md`, semantically independent from upstream-derived Moreh operational guidance. Upstream reconciliation must preserve their meaning and position unless the user explicitly requests a change.
- Keep shared skills in the `skills` submodule backed by `preference-kim/my-claude-skills`.
- Discover the shared file and skill through relative repository symlinks plus host-global Codex and Claude links.
- Run synchronization from the first agent session on each local calendar day; do not depend on cron, launchd, or a continuously running process.
- Publish personal agent-file updates directly to `main` in the skills repository first and the dotfiles repository second.

## Intentional divergences

- Use `sunho/` rather than `heehoon/` as the default feature-branch prefix.
- Allow tray-scoped Galaxy locking, reset, and `TT_VISIBLE_DEVICES` configuration when the matching tray lock is held. Do not import upstream's blanket prohibition on tray-scoped work.
- Use the portable repository layout above rather than upstream-specific `~/.files`, Moreh-server paths, or whole-directory Codex skill links.
- Preserve the daily semantic reconciliation workflow in the local `agent-update` skill instead of replacing it with upstream's simpler pull-only workflow.

These are policy differences, not frozen text. Reconcile upstream changes that improve their safety or clarity without reversing the local decision.
