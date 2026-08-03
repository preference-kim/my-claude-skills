# Upstream Agent Guidance

## Reviewed source

- Repository: `https://github.com/csehydrogen/.files.git`
- Branch: `master`
- Reviewed commit: `ac034f1387bca107dcb71595910d5a43eb9db60c`
- Instruction path: `AGENTS.md`
- Skill path: `skills/agent-update/SKILL.md`
- Skill scope: every file below `skills/`, including manifest, resource, and script additions, removals, renames, and content changes.

## Adopted skill mappings

- `skills/agent-update/` → `<dotfiles>/skills/agent-update/`
- `skills/gh-review-own-pr/` → `<dotfiles>/skills/gh-review-own-pr/`

Advance the reviewed commit only after the instruction file, updater skill, and full upstream skill manifest inventory at the new commit have been inspected and every applicable change has been reconciled or consciously covered by an intentional divergence.

## Local design

- Keep `AGENTS.md` at the dotfiles root as the canonical instruction file.
- Keep the user-owned stable working principles at the top of `AGENTS.md`, semantically independent from upstream-derived Moreh operational guidance. Upstream reconciliation must preserve their meaning and position unless the user explicitly requests a change.
- Keep shared skills in the `skills` submodule backed by `preference-kim/my-claude-skills`.
- Discover the shared instruction file through relative repository symlinks plus host-global instruction links. Expose every shared skill through per-skill links inside the real `~/.codex/skills` and `~/.claude/skills` directories so host-local skills and overrides can coexist. Do not keep independent tool-specific clones or whole-directory skill links.
- Track locally maintained or locally adapted skills directly. A verbatim third-party skill may remain a nested submodule when its independent provenance and update boundary are useful; `humanizer` is the current instance of this policy.
- Run synchronization from the first agent session on each local calendar day; do not depend on cron, launchd, or a continuously running process.
- Publish personal agent-file updates directly to `main` in the skills repository first and the dotfiles repository second.
- Monitor the full upstream skill manifest inventory. Adopt compatible skills through explicit source mappings and preserve a documented rationale for any non-adoption.

## Intentional divergences

- Use `sunho/` rather than `heehoon/` as the default feature-branch prefix.
- Allow tray-scoped Galaxy locking, reset, and `TT_VISIBLE_DEVICES` configuration when the matching tray lock is held. Do not import upstream's blanket prohibition on tray-scoped work.
- Use the portable canonical-submodule and per-skill-link layout above rather than upstream-specific `~/.files`, Moreh-server paths, tool-specific clones, or whole-directory Codex or Claude skill links.
- Preserve the daily semantic reconciliation workflow in the local `agent-update` skill instead of replacing it with upstream's simpler pull-only workflow.
- Keep a curated local skill set rather than mirroring upstream skills wholesale. At the reviewed baseline, `caveman` is not adopted because persistent compressed speech can undermine the local completeness requirements; `gh-review-other-pr` is not adopted because its temporary clone/worktree guidance must first be reconciled with the local worktree restriction. `gh-review-own-pr` is adopted through the mapping above.

These are policy differences, not frozen text. Reconcile upstream changes that improve their safety or clarity without reversing the local decision.
