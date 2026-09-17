---
name: skill-maker
description: Use to create, critique, refine, or maintain agent SKILL.md files, skill folders, or shared harness structure across Claude and Codex. Not for code review or critique of an implementation plan.
---

# Skill Maker

## Resolve ownership and routing first

Refine an existing target when named; create only for a new capability. Resolve
symlinks, repository ownership, installed copies, and the target runtime before
choosing a path. Resolve installation and publication targets separately: a skill
discovered in a project may belong to a personal repository. Never default to a
Claude-only user directory. For shared skills,
edit the canonical source and expose it through each configured runtime adapter.
Preserve unique local overrides and dirty repositories; equal names do not prove
equivalent behavior. Ask only when scope or ownership cannot be established.

Before drafting a new skill, establish its name (matching its directory), purpose,
and adjacent capabilities. Before changing any routing description, prepare the
[routing eval pack](assets/routing-eval-template.md): at least three positive
utterances, one negative, and one adjacent collision. Record expected changes
from the old description. Derive examples from the task when clear; ask only for
missing intent. Descriptions say when to load, preferably in 50 words or fewer.

## Refine against failures

Draft in working memory, then read [anti-patterns](references/anti-patterns.md)
and critique in its listed order: routing failures invalidate later prose polish.
Use [template](assets/skill-template.md) for a new skill unless the target runtime
requires another format. Keep name/description as the default frontmatter; add
platform metadata only for a concrete need.

Keep only instructions whose absence causes a plausible task failure. Make the
applicability, required action, and completion condition understandable without
forcing every rule into a template. Retain local contracts and fragile flags;
remove generic tutorials, system-prompt recaps, and repeated conclusions.

Use short sentences and focused bullets that preserve the necessary reasoning.
Keep a flat body unless conditional references, scripts, or assets reduce loading
or reconstruction. State each reference's purpose and read-before-action trigger;
verify that the intended runtime or isolated reader can access its requirements.
Do not move everything into an unconditionally loaded file.

For a harness, separate always-loaded policy, discovery descriptions, task bodies,
and conditional resources. Map every existing requirement to its retained owner.
Consolidate duplicates without weakening semantics; flag contradictions instead
of silently changing behavior. Keep provider details in adapters and maintain
routing cases across Claude and Codex. Measure each loading tier separately.
Keep internal task-derived fixtures, results, inventories, and audits outside
public worktrees, in the local agent-update state directory. Reusable published examples must be synthetic or explicitly cleared
for the destination audience; do not send internal evidence to another service
for evaluation without authorization.

## Apply and verify

Show concrete edits and routing deltas, not generic critique. If implementation is
already authorized, write the scoped changes and make the resulting diff reviewable;
otherwise present the full candidate bundle and wait for explicit write approval.
Do not request approval again for work already authorized in the session.

Validate frontmatter, reference paths, requirement coverage, and routing positives,
negatives, and collisions. For shared harness changes, compare old and revised
guidance on the same task-relevant cases in fresh Claude and Codex sessions.
For general principles, include different document types and a simple request
to detect imposed templates or unnecessary work. Evaluate retained meaning and
required behavior, not just length or keyword presence. Disclose unavailable
models/authentication and distinguish supplied-guidance judgments from observed
live routing. Re-read written files and report limits.

Turn reusable failures into small regression cases and consolidate them with the
existing owner. Do not append incident histories or duplicate gotchas. Add only
the shortest rule needed to prevent recurrence. Preserve local indexes unless
the authorized scope includes their maintenance.
