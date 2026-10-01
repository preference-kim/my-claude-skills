# Upstream Agent Guidance

## Reviewed source

- Repository: `https://github.com/csehydrogen/.files.git`
- Branch: `master`
- Reviewed commit: `41f39935fe53ddd8fc0c838067c38c1fbe02f7f2`
- Instruction path: `AGENTS.md`
- Skill path: `skills/agent-update/SKILL.md`
- Skill scope: every file below `skills/`, including manifest, resource, and script additions, removals, renames, and content changes.

## Adopted skill mappings

- `skills/agent-update/` → `<dotfiles>/skills/agent-update/`
- `skills/gh-review-other-pr/` → `<dotfiles>/skills/gh-review-other-pr/`
- `skills/gh-review-own-pr/` → `<dotfiles>/skills/gh-review-own-pr/`

Advance the reviewed commit only after the instruction file, updater skill, and full upstream skill manifest inventory at the new commit have been inspected and every applicable change has been reconciled or consciously covered by an intentional divergence.

## Local design

- Keep `AGENTS.md` at the dotfiles root as the canonical instruction file. Keep its always-loaded policy concise; shared personal guidance lives in conditionally loaded `agent-guidance/` or skill references. Preserve the approved Moreh/TT-Metal development knowledge under `agent-guidance/tt-metal/`, with mandatory triggers in AGENTS.md. New private project details and local evidence stay outside public worktrees. Preserve requirement meaning and reachability, not monolithic placement.
- Keep the user-owned stable working principles at the top of `AGENTS.md`, semantically independent from upstream-derived Moreh operational guidance. Upstream reconciliation must preserve their meaning and position unless the user explicitly requests a change.
- Keep shared skills in the `skills` submodule backed by `preference-kim/my-claude-skills`.
- Keep the gitignored per-host `agent-file-sync.local.yaml` modes and exact `moreh_dev_root` validation. Separate instruction location from skill installation scope: `.installation-policy.json` maps every approved skill to `user` or `moreh-dev`. Both modes install user skills at `~/.agents/skills` (Codex) and `~/.claude/skills` (Claude). Only `moreh-dev` installs project skills at the configured checkout’s `.agents/skills` and `.claude/skills`. Keep mode-specific instruction locations unchanged, and exclude project-only skills in `host-global`. Use real discovery roots and canonical per-skill links; preserve unrelated installations. An invalid project root blocks project work, not independent user installation, and prevents a successful refresh stamp.
- Track locally maintained or adapted skills directly unless they have a separate authoritative repository. Preserve that repository as a nested submodule: `stop-bullshit` is user-owned at `preference-kim/stop-bullshit`; `humanizer` is a verbatim third-party skill. Publish changed user-owned nested skills before this repository, then publish the dotfiles pointer.
- Run synchronization from the first agent session on each local calendar day; do not depend on cron, launchd, or a continuously running process.
- Publish personal agent-file updates directly to `main` in the skills repository first and the dotfiles repository second. The configured development checkout receives ignored local links only; it is not a publication destination. Preserve tracked project skills unless the user explicitly requests that project contribution.
- Monitor the full upstream skill manifest inventory. Adopt compatible skills through explicit source mappings and preserve a documented rationale for any non-adoption.

## Intentional divergences

- Use `sunho/` rather than `heehoon/` as the default feature-branch prefix.
- Keep host-local mode and checkout configuration separate from the shared installation-scope manifest. General-purpose skills are available outside Moreh even on a `moreh-dev` host; project-dependent skills stay local to the configured checkout. Use the portable per-skill layout above rather than upstream-specific checkout paths or whole-directory clones. Follow `installation.md` for canonical-path reference resolution and verified legacy migration; do not restore the former ban on all global entries in `moreh-dev` or the obsolete cleanup of supported `~/.agents/skills` links.
- Permit `git worktree` only for static code analysis or documentation at a specific HEAD; keep builds and device-backed work in the primary checkout. Adapt upstream primary-checkout guidance to this narrower local exception.
- Preserve the daily semantic reconciliation workflow in the local `agent-update` skill instead of replacing it with upstream's simpler pull-only workflow.
- Keep a curated local skill set rather than mirroring upstream skills wholesale. `caveman` is not adopted because persistent compressed speech can undermine the local completeness requirements. The two GitHub review skills are adopted through local counterparts that preserve the primary-checkout, branch, and read-only/write-boundary rules above.
- Unlike upstream's chat-only `gh-review-other-pr`, write validated findings as concise Korean inline comments in the current viewer's unsubmitted pending review. Use the shared `humanizer` skill as the final prose-editing pass, then verify each stored comment's clarity, concision, and structure before reporting back. Keep leaf reviewers and validation read-only, authorize no other GitHub mutation, and never publish or submit the review; this places the final feedback on the relevant diff lines while preserving user control over submission.

- Preserve the shared Claude/Codex harness structure: one owner per contract, narrow routing descriptions with positive/negative/adjacent cases, and runtime details in adapters. Reconcile changed upstream requirements into their owning reference rather than restoring an always-loaded catalog. Shared skill discovery uses tracked files and approved gitlinks only. Internal maintenance and evaluation evidence stays outside both worktrees and skill discovery. Do not restore a tracked evidence directory or treat personal publication authority as permission to disclose project information.

- The dedicated `plan-review` skill is retired at the user's request. Do not recreate its discovery entries or mandatory opposite-family review workflow during synchronization. Ordinary plan critique uses the agent's normal capabilities.

- Preserve accurate reasoning, explicit understanding of the task and relevant
  context before consequential action, and reader-oriented documentation in the
  always-loaded reasoning and delivery principles. Keep essential explanations
  in the document, match evidence to claims, and preserve minimal verified
  procedures. Apply the same principles to instruction documents; keep task-only
  formats in their owning skills. Preserve the PR local-artifact prohibition and
  the explicit same-environment handoff exception. Keep philosophical attribution
  out of AGENTS.md. The separately maintained
  `stop-bullshit` skill owns the detailed check; keep that single name throughout
  the harness. It is distinct from the prose-editing role of `humanizer`. Preserve
  the AGENTS trigger for user reactions indicating bullshit, evasion, or unearned
  certainty. PR review checks both source material and feedback after prose
  editing, including isolated reviewer prompts.

These are policy differences, not frozen text. Reconcile upstream changes that improve their safety or clarity without reversing the local decision.
