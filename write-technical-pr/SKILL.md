---
name: write-technical-pr
description: Use to draft, revise, or audit a technical GitHub PR description and its supporting evidence. Not for reviewing code, submitting a branch, or independently critiquing an implementation plan.
---

# Write Technical PR

Read [description policy](references/policy.md) before drafting any PR body.
For experiments, quantitative claims, correctness coverage, or figures, also read
[evidence contracts](references/evidence.md). Do not run experiments or modify
source, tests, branches, or benchmark artifacts merely to write a description.

## Establish the current argument

Identify repository, PR, base/head, audience, and review decision. Inspect the actual
diff and only the evidence needed to substantiate retained behavior. Read the live
body before revising so concurrent or integration-owned content is not overwritten.
Preserve an explicitly requested structure when semantically valid; reshape stale
sections instead of appending patch notes.

Start with `## Korean Summary`: problem, retained solution, and concrete result
using established codebase terms. Add only useful topics: interfaces/contracts,
implementation, correctness, performance, resources, integration, remaining limits.
Define inputs/outputs, ownership, shapes, invariants, defaults, unsupported cases,
dataflow, synchronization, and material allocation assumptions where relevant.

Report only the current design relative to the base and final retained results.
Exclude branch evolution, rejected probes, transient bugs, retries, and rerun
chronology. A baseline is a direct matched comparison, never a development story.
If measured source differs from PR head, put the narrow qualifier beside the claim
or omit it. Do not use candidate allocations as current resource usage.

## Verify and publish

- Transfer every material fact into the body; local artifacts are not citations.
- Keep the few mechanisms that explain the design/results; fold small refinements
  into their owning section. No superseded experiments or raw diagnostic logs.
- Check every headline, table, formula, link, source identity, quantitative claim, and
  caption against evidence. Ensure summary, correctness, performance, and
  integration scopes agree. State missing validation without inventing success.
- After the last prose edit, apply
  [stop-bullshit](../stop-bullshit/SKILL.md) on the source claims and final body;
  when auditing a description, also check your review comments themselves.
- Check policy and applicable evidence contracts, then update the live body only
  when authorized. Re-read it to verify Markdown and concurrent content survived.
