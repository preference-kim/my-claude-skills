# Upstream Agent Guidance

## Reviewed source and mappings

- Repository: `https://github.com/csehydrogen/.files.git`; branch: `master`.
- Reviewed commit: `a02946d21773e4171b6d0627e159f624f526809c`.
- Instruction: `AGENTS.md`; updater: `skills/agent-update/SKILL.md`.
- Inventory: every file under `skills/`, including added, removed, renamed and
  changed manifests, resources and scripts.

| Upstream source | Local owner |
| --- | --- |
| `skills/agent-update/` | `<dotfiles>/skills/agent-update/` |
| `skills/gh-review-other-pr/` | `<dotfiles>/skills/gh-review-other-pr/` |
| `skills/gh-review-own-pr/` | `<dotfiles>/skills/gh-review-own-pr/` |
| `skills/moreh-tt-development/` | `<dotfiles>/agent-guidance/tt-metal/`, not a discovered skill |

Advance the reviewed commit only after inspecting the instruction, updater and
full skill inventory and reconciling each applicable change or documenting its
intentional divergence. New skills require an explicit adoption/non-adoption
decision; the local set is curated, not a mirror.

## Preserve these design decisions

These decisions preserve behavior, not frozen wording. Integrate compatible
upstream improvements into the owning contract and retain conditional access
for isolated consumers. Read the referenced owner before changing that contract.

- **Canonical policy:** dotfiles-root `AGENTS.md` is shared by Claude/Codex.
  Its user-owned stable principles stay at the top, independent of Moreh
  guidance unless the user requests change. Keep reasoning and reader-oriented
  delivery principles there, task formats in skills, provider details in
  adapters, and philosophical attribution out. Each contract has one owner.
- **Installation:** [preflight](preflight.md),
  [installation](installation.md) and
  [entry-point policy](entry-point-policy.md) own host-local modes, exact
  `moreh_dev_root`, portable per-skill links, user/project scope and migration.
  Both modes retain user skills for both runtimes. Do not ban user-scope skills
  in `moreh-dev` or remove supported `~/.agents/skills` links. Instruction files
  remain in the configured project only in that mode.
  Discovery includes only approved tracked sources/gitlinks, never internal
  audits or local evidence.
- **Source ownership:** shared skills live in `preference-kim/my-claude-skills`.
  Maintain/adapt skills directly unless another authoritative repository owns
  them. `stop-bullshit` remains user-owned at `preference-kim/stop-bullshit`;
  `humanizer` and `simple-english` remain unchanged vendor submodules.
  SimpleEnglish's source is `https://github.com/AminBlg/SimpleEnglish.git`,
  with nested `skill-path` in `.gitmodules`. Both vendor skills are pinned
  references, excluded from discovery and routine writing. `technical-communication`
  owns technical prose; `stop-bullshit` owns explicit audits and recovery.
  Preserve that separation when reconciling upstream changes. Read
  [reference maintenance](reference-maintenance.md) before checking or adopting
  vendor changes; update notices do not authorize adoption.
- **Maintenance:** retain [preflight](preflight.md)'s session-driven daily
  semantic reconciliation and installed-CLI updates, rather than upstream's
  pull-only workflow. [Private synchronization](private-sync.md) runs approved
  current-owner SSH on every refresh; other private scopes remain explicit.
  Shell startup and `clear` never fetch/deploy. No cron, launchd or daemon is
  required.
- **Git and publication:** `<dotfiles>/agent-guidance/version-control.md` owns
  local `sunho/` feature branches and worktrees limited to static analysis/docs
  at a specific HEAD. Builds/device work stay in the primary checkout.
  [Publication](publication.md) publishes user-owned children before personal
  parents on `main`; project installation grants no project publication or
  disclosure authority. `<dotfiles>/PUBLICATION.md` owns audience/history
  review and local-only evidence.
- **Claude authentication:** `<dotfiles>/agent-guidance/claude-auth.md` owns
  CLI-managed authentication and child-only override removal, instead of an
  upstream static OAuth-token file.
- **Review workflows:** both GitHub skills preserve local Git and write
  boundaries. Unlike upstream chat-only review, `gh-review-other-pr` stores
  validated concise Korean inline findings in the viewer's unsubmitted pending
  review. Leaf reviewers/validation stay read-only; no other GitHub mutation
  or submission is authorized. Preserve separate technical prose review, followed by
  `stop-bullshit` checks of material and feedback, including isolated prompts.
  Preserve AGENTS' PR ban on inaccessible local evidence and same-environment
  handoff exception. Keep `stop-bullshit` as the single detailed audit owner
  and its user-challenge trigger; prose editing remains a separate role.
  `gh-review-own-pr` owns the confirmed Copilot quota exception; other missing
  reviewer results still require explicit authorization to continue.
- **TT knowledge:** public `agent-guidance/tt-metal/` retains API/measurement
  guidance and mandatory policy loading, not team operating values. Private
  `team-development.md` owns build/test conventions, reservation and reset
  procedures, recovery budgets, and project helper integrations. Preserve their
  behavior through the loader; never restore private settings to public files
  when reconciling upstream. Public deployment helpers consume private
  `deployment.json` under the guarded deployment contract. Personal Git settings
  and existing history stay unchanged. New project-derived details require
  audience authorization. Do not adopt a blanket replacement of explicit device
  deallocation with Python name deletion; inspect ownership and release timing.
- **Non-adoption:** upstream removed `caveman`; it was never adopted because
  persistent compressed speech conflicts with completeness. The user retired
  `plan-review`; do not restore its discovery entries or opposite-family
  review mandate. Ordinary plan critique uses normal agent capabilities.
