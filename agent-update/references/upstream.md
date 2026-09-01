# Upstream Agent Guidance

## Reviewed source

- Repository: `https://github.com/csehydrogen/.files.git`
- Branch: `master`
- Reviewed commit: `0348a20bcebf494f3ba42dc601d8675bf2784d4f`
- Instruction path: `AGENTS.md`
- Skill path: `skills/agent-update/SKILL.md`
- Skill scope: every file below `skills/`, including manifest, resource, and script additions, removals, renames, and content changes.

## Adopted skill mappings

- `skills/agent-update/` → `<dotfiles>/skills/agent-update/`
- `skills/gh-review-other-pr/` → `<dotfiles>/skills/gh-review-other-pr/`
- `skills/gh-review-own-pr/` → `<dotfiles>/skills/gh-review-own-pr/`

Advance the reviewed commit only after the instruction file, updater skill, and full upstream skill manifest inventory at the new commit have been inspected and every applicable change has been reconciled or consciously covered by an intentional divergence.

## Local design

- Keep `AGENTS.md` at the dotfiles root as the canonical instruction file.
- Keep the user-owned stable working principles at the top of `AGENTS.md`, semantically independent from upstream-derived Moreh operational guidance. Upstream reconciliation must preserve their meaning and position unless the user explicitly requests a change.
- Keep shared skills in the `skills` submodule backed by `preference-kim/my-claude-skills`.
- Discover the shared instruction files and skills through a per-host layout mode, `host-global` or `moreh-dev`, recorded in `agent-file-sync.local.yaml` at the dotfiles root: a gitignored, host-local file (templated by the tracked `agent-file-sync.example.yaml`) that never syncs through git, so no host's mode or target is visible or settable from another host. `host-global` exposes them at `~/.codex`/`~/.claude` entry points, with per-skill links inside the real `~/.codex/skills`/`~/.claude/skills` directories; `moreh-dev` exposes the same entry points and per-skill links inside the host-specific Git checkout named by the required `moreh_dev_root`, with no host-global installation. Resolve relative targets from the dotfiles root, accept explicit absolute targets, validate the exact Git root, and never search for or create a target. Do not keep independent tool-specific clones or whole-directory skill links in either mode.
- Track locally maintained or locally adapted skills directly. A verbatim third-party skill may remain a nested submodule when its independent provenance and update boundary are useful; `humanizer` is the current instance of this policy.
- Run synchronization from the first agent session on each local calendar day; do not depend on cron, launchd, or a continuously running process.
- Publish personal agent-file updates directly to `main` in the skills repository first and the dotfiles repository second.
- Monitor the full upstream skill manifest inventory. Adopt compatible skills through explicit source mappings and preserve a documented rationale for any non-adoption.

## Intentional divergences

- Use `sunho/` rather than `heehoon/` as the default feature-branch prefix.
- Use a gitignored, per-host `agent-file-sync.local.yaml` to choose between the `host-global` and `moreh-dev` layouts and to name the required `moreh_dev_root` for `moreh-dev`, rather than fixing a layout or checkout path in `AGENTS.md`/`SKILL.md`: because the file never syncs through git, no agent-update run on any host can read, set, or redefine another host's mode or target; each host's choice is made only on that host. `agent-file-sync.example.yaml` is the tracked template new hosts copy from. Use the portable per-skill-link layout above rather than upstream-specific `~/.files`, Moreh-server paths, tool-specific clones, or whole-directory Codex or Claude skill links.
- Permit `git worktree` only for static code analysis or documentation at a specific HEAD; keep builds and device-backed work in the primary checkout. Adapt upstream primary-checkout guidance to this narrower local exception.
- Preserve the daily semantic reconciliation workflow in the local `agent-update` skill instead of replacing it with upstream's simpler pull-only workflow.
- Keep a curated local skill set rather than mirroring upstream skills wholesale. `caveman` is not adopted because persistent compressed speech can undermine the local completeness requirements. The two GitHub review skills are adopted through local counterparts that preserve the primary-checkout, branch, and read-only/write-boundary rules above.
- Unlike upstream's chat-only `gh-review-other-pr`, write validated findings as concise Korean inline comments in the current viewer's unsubmitted pending review. Keep leaf reviewers and validation read-only, authorize no other GitHub mutation, and never publish or submit the review; this places the final feedback on the relevant diff lines while preserving user control over submission.

These are policy differences, not frozen text. Reconcile upstream changes that improve their safety or clarity without reversing the local decision.
