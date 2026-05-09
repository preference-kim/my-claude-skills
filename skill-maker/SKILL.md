---
name: skill-maker
description: Use when the user asks to create, scaffold, draft, critique, refine, or improve a Claude Code SKILL.md or skill folder.
---

# Skill Maker

Route the request before doing anything else. Use REFINE when the user names an existing skill, names a filesystem path, or uses any of: critique, review, refine, improve, tighten, fix. Use CREATE when the user asks to make, create, scaffold, draft, or write a new skill. If both modes are plausible, ask one disambiguation question.

"review" is intentionally absent from the description (collides with `plan-review`, `review`, `security-review`) but kept here as a synonym once skill-maker is loaded. Do not "reconcile" by adding it back to the description.

## CREATE Mode

Interview before drafting. Gather:

1. Skill name, normalized to lowercase kebab-case. The folder name and frontmatter `name` must match.
2. One-sentence purpose.
3. Three concrete user utterances that should load the skill, plus one adjacent negative utterance that should not.

Before drafting, check whether `~/.claude/skills/<name>/` already exists. If it exists, do not overwrite it. Ask whether to switch to REFINE mode for that skill or choose a different name.

Draft in this order:

1. Write the description first. It is the routing trigger, not internal documentation. Prefer "Use when..." or "Load when..." phrasing, target 50 words or fewer, cover the positive utterances, and exclude the negative utterance.
2. Write the body for another agent, not for a human reader. Lead with the gotchas, decisions, and failure modes the model would plausibly miss.
3. Keep obvious model knowledge out of the body. Do not restate generic shell, git, editing, or system-prompt behavior.
4. Decide whether extra files are needed. Default to a flat `SKILL.md`; propose `references/`, `scripts/`, or `assets/` only for heavy conditional material, deterministic code, or reusable output resources.
5. Choose frontmatter style. Default to minimal (`name` + `description`); see `~/.claude/skills/plan-review/SKILL.md`. Add `allowed-tools`, `license`, `version`, or compatibility metadata only when genuinely needed; see `~/.claude/skills/humanizer/SKILL.md`.

## REFINE Mode

Resolve the target skill before critique:

- If the user provided an absolute path, `~` path, or relative path, resolve it to a concrete `SKILL.md`.
- If the user provided a skill name, check `~/.claude/skills/<name>/SKILL.md`.
- If the name is fuzzy, search `~/.claude/skills/*/SKILL.md` and ask only if multiple plausible matches remain.

Read the target file and inspect any bundled files only when they affect the critique.

## Pipeline

Both modes follow the same order. Do not skip or reorder.

1. **Draft.** Produce a candidate SKILL.md (CREATE) or revision (REFINE) in working memory. Do not write to disk.
2. **Critique.** Read `references/anti-patterns.md` and run every section in order, top to bottom. Earlier failures invalidate later checks; fix them before continuing. Prioritize Description As Documentation and Unevaluated Description Changes because the description is the routing layer and is paid for in every session.
3. **Apply.** Edit the in-memory draft to fix every concrete issue. Report critique as concrete edits, not vague advice:
   - `description: rewrite "...old..." -> "...new..." because the old version documents internals instead of routing intent`
   - `Body / Drafting: cut paragraph about generic git workflow; the base agent already knows it`
   - `Body / Resources: move API status codes to references/api-errors.md because they are heavy and conditional`
4. **Show.** Present findings + the full revised `SKILL.md` in a fenced `markdown` block.
5. **Approve.** Wait for explicit user confirmation before any disk write. This is the only approval gate; do not ask earlier.
6. **Write.** On approval, write to `~/.claude/skills/<name>/SKILL.md` (CREATE) or overwrite the resolved target path (REFINE). Also write any approved bundled files. Do not edit `~/.claude/skills/README.md`; mention it as a manual follow-up.
7. **Verify.** Re-read the written file and summarize the final state.

Do not add frontmatter fields just because another skill has them. Treat any description change as a routing change that must be tested against positive and negative utterances before step 5.
