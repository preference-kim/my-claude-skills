---
name: skill-maker
description: Use to create, critique, refine, or maintain agent SKILL.md files, skill folders, or shared harness structure across Claude and Codex. Not for code review or critique of an implementation plan.
---

# Skill Maker

## Establish ownership and routing

Refine the named target. Create a skill only for a new capability. Resolve
symlinks, repository ownership, installed copies, and runtime before choosing a
path. Installation and publication can have different owners. Edit shared skills
at their canonical source and expose them through configured runtime adapters.
Preserve distinct local overrides and unrelated changes. Ask only about unresolved
scope or ownership.

Before creating a skill, establish its directory-matching name, purpose, and
adjacent capabilities. Before any description change, prepare the
[routing cases](assets/routing-eval-template.md): three positives, one negative,
and one adjacent collision, with expected differences from the old description.
Derive cases from the request and clarify only missing intent. Descriptions state
when to load, preferably in 50 words or fewer.

## Design the loaded instructions

Read [anti-patterns](references/anti-patterns.md) before accepting a draft and apply
the checks in order. Use the [template](assets/skill-template.md) for a new skill
unless its runtime requires another format. Default frontmatter is name and
description. Add platform metadata only for a concrete need.

Keep rules whose absence permits a plausible task failure. Express scope, entry
conditions, required behavior, and completion criteria. Preserve local contracts
and fragile flags. Consolidate overlapping restrictions under their governing
condition instead of accumulating incident-specific exceptions.

For a harness, map each existing requirement to its retained owner. Preserve
semantics and report contradictions. Separate always-loaded policy, discovery
descriptions, task bodies, and conditional resources. Keep provider details in
adapters. State when and why each reference is needed, including requirements
for isolated readers. Measure each loading tier and full task paths. A shorter
body does not reduce context if its references are always loaded.

Keep internal fixtures, inventories, audits, and results outside public worktrees
in the local agent-update state directory. Published examples must be synthetic
or cleared for that audience. Evaluation on another service requires authorization
for any internal evidence supplied to it.

## Apply and verify

When implementation is authorized, write the scoped changes and inspect the diff.
Otherwise present the concrete bundle for write approval. Do not request approval
again for an already authorized action.

Check frontmatter, links, requirement coverage, and routing cases. Compare old
and revised shared guidance on the same relevant cases in fresh Claude and Codex
sessions. For general principles, include different document types and a simple
request to detect imposed templates or unnecessary work. Evaluate behavior and
retained meaning, not just length or keywords. Distinguish supplied-guidance
judgments from live routing, and report unavailable models or authentication.

Re-read the saved files and report limits. Capture reusable failures as small
regression cases under their existing owner. Add only the shortest necessary
rule. Preserve local indexes unless their maintenance is authorized.
