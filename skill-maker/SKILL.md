---
name: skill-maker
description: Use when the user asks to create, scaffold, draft, critique, refine, or improve a Claude Code SKILL.md or skill folder.
---

# Skill Maker

Route the request before doing anything else. Use REFINE when the user names an existing skill, names a filesystem path, or uses any of: critique, review, refine, improve, tighten, fix. Use CREATE when the user asks to make, create, scaffold, draft, or write a new skill. If both modes are plausible, ask one disambiguation question.

"review" is intentionally absent from the description (collides with `plan-review`, `review`, `security-review`) but kept here as a synonym once skill-maker is loaded. Do not "reconcile" by adding it back to the description.

## CREATE Mode

Interview before drafting. Gather only what changes routing or content:

1. Skill name. The folder name and frontmatter `name` must match.
2. One-sentence purpose.
3. Three concrete user utterances that should load the skill, one negative utterance that should not, and any adjacent skill likely to collide.

Before drafting, check whether `~/.claude/skills/<name>/` already exists. If it exists, do not overwrite it. Ask whether to switch to REFINE mode for that skill or choose a different name.

Create a routing eval pack from `assets/routing-eval-template.md` before drafting. The description is not acceptable until the pack can explain why positives route here and negatives do not.

Draft from `assets/skill-template.md` unless the target system requires a different format. Write the description first: it is the routing trigger, not internal documentation. Prefer "Use when..." or "Load when..." phrasing, target 50 words or fewer, cover the positive utterances, and exclude the negative utterance.

Write the body for another agent, not for a human reader. Lead with gotchas, decisions, and failure modes the model would plausibly miss. Keep obvious model knowledge out of the body. Do not restate generic shell, git, editing, or system-prompt behavior.

Default to a flat `SKILL.md`. Add `references/`, `scripts/`, or `assets/` only when the material is heavy and conditional, deterministic enough to reuse, or an output resource the agent should fill rather than reconstruct.

## REFINE Mode

Resolve the target skill, then inspect the target `SKILL.md` and bundled files only when they affect the critique.

If the description will change, create or update a routing eval pack from `assets/routing-eval-template.md` before accepting the rewrite. Treat the old and new descriptions as behaviorally different and record the expected routing delta.

## Pipeline

Both modes follow the same order. Do not skip or reorder.

1. **Route.** Choose CREATE or REFINE and resolve the target or intended name.
2. **Eval Pack.** Write or update a routing eval pack in working memory. Do not write it to disk unless the user approves the final bundle.
3. **Draft.** Produce a candidate `SKILL.md` (CREATE) or revision (REFINE) in working memory. Do not write to disk.
4. **Critique.** Read `references/anti-patterns.md` and run every section in order, top to bottom. Earlier failures invalidate later checks; fix them before continuing. Prioritize routing failures because the description is paid for before the body is available.
5. **Apply.** Edit the in-memory draft to fix every concrete issue. Report critique as concrete edits, not vague advice:
   - `description: rewrite "...old..." -> "...new..." because the old version documents internals instead of routing intent`
   - `Body / Drafting: cut paragraph about generic git workflow; the base agent already knows it`
   - `Body / Resources: move API status codes to references/api-errors.md because they are heavy and conditional`
6. **Show.** Present findings, the routing eval pack summary, candidate gotchas, and the full revised `SKILL.md` in a fenced `markdown` block.
7. **Approve.** Wait for explicit user confirmation before any disk write. This is the only approval gate; do not ask earlier.
8. **Write.** On approval, write to `~/.claude/skills/<name>/SKILL.md` (CREATE) or overwrite the resolved target path (REFINE). Also write any approved bundled files. Do not edit `~/.claude/skills/README.md`; mention it as a manual follow-up.
9. **Verify.** Re-read the written files and summarize the final state.
10. **Capture Gotchas.** If critique found a reusable failure mode, ask whether to append it to the target skill's gotchas or to `skill-maker/references/anti-patterns.md`.

Do not add frontmatter fields just because another skill has them. Default to minimal (`name` + `description`); add `allowed-tools`, `license`, `version`, or compatibility metadata only when genuinely needed.
