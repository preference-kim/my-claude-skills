---
name: write-technical-pr
description: Draft, restructure, audit, and update technical GitHub pull-request descriptions as concise current-design documents. Use when creating or revising a PR body, especially for systems, kernel, distributed, performance, or model-integration work that must explain interfaces, invariants, implementation, correctness, resource limits, benchmarks, figures, and remaining constraints.
---

# Write Technical PR

Write the PR description as a decision document for reviewers. Present the
current change, its evidence, and its limits as one coherent argument. Do not
turn the PR body into an experiment log or edit history.

## Establish the review scope

1. Identify the repository, PR, base, head, audience, and decision the reviewer
   must make.
2. Inspect the actual diff and the source, design documents, tests, benchmark
   artifacts, and integration reports needed to verify the claims.
3. Separate retained and validated behavior from work in progress, rejected
   probes, historical baselines, and unverified plans.
4. When revising an existing PR, read the live body before editing. Compare it
   with any local draft so that concurrent or integration-owned updates are not
   overwritten.
5. Preserve an explicitly requested structure when it remains semantically
   valid. Reshape stale sections instead of appending a revision narrative.

Do not modify source code, tests, branches, or benchmark artifacts merely to
write a PR description unless the user separately requests those changes.

## Build a current-state argument

Adapt the structure to the change. Use only sections that help the reviewer,
typically:

- **Summary:** State the purpose, boundary, target, and headline evidence.
- **Interface and contracts:** Define inputs, outputs, ownership, shapes,
  invariants, defaults, and unsupported configurations.
- **Implementation:** Explain the current dataflow, partitioning, resource
  ownership, synchronization, and major design decisions.
- **Correctness:** State acceptance criteria, tested source, coverage, and
  results.
- **Performance:** State the benchmark protocol, target model, measurements,
  component analysis, and figures.
- **Resource limits:** Name the concrete allocations and assumptions behind
  memory, bandwidth, or capacity bounds.
- **Integration evidence:** Report model- or deployment-level validation when
  it materially expands the operator-level evidence.
- **Remaining constraints:** Include only unresolved issues that affect review,
  adoption, or the next decision.

Integrate new information into the section that owns its meaning. Do not add a
"what changed since the previous version" section unless the user explicitly
requests release notes.

## Maintain scientific evidence boundaries

Classify each technical claim before writing it:

- **Measured:** Observed directly under a stated source and workload.
- **Derived:** Calculated from measured inputs, such as a residual or
  accumulated estimate.
- **Model-derived:** Calculated from a hardware, cost, or capacity model.
- **Hypothesis:** A falsifiable explanation awaiting a stated experiment.
- **Decision:** A selected design justified by explicit criteria.

Never label derived or model-derived values as measured. State the source
identity, workload, units, denominator, participating resources, and protocol
needed to interpret a quantitative claim. If evidence is stale or covers a
narrower source or test scope, say so plainly or remove it.

Keep facts and limitations adjacent. Do not rely on a distant disclaimer to
correct an over-broad table or headline.

## Present performance at the right levels

Keep system-level evaluation and component diagnosis distinct.

### System-level result

- Define the full measured boundary.
- Define the target or expected-time model before reporting achievement.
- State the compute, communication, or memory assumptions used by the model.
- Calculate `achievement` only against that stated target model.

### Component analysis

- Compare each component with the theoretical peak of the resources that
  actually execute it.
- State the participating core, link, bank, or device count.
- Use operation-weighted peaks for mixed-operation components and name the
  included operations.
- Report useful payload and directionality for communication bandwidth.
- Treat overlapping intervals as intervals; never sum them into latency.
- Leave utilization blank when no defensible peak or work count exists.

Do not mix target-model achievement with theoretical-peak utilization in one
column or describe one as the other.

## Use quantitative information economically

- Preserve enough precision for acceptance thresholds, reproducibility, and
  close A/B decisions.
- Round presentation values when extra digits do not change the conclusion.
- Keep exact byte counts, shapes, and contractual constants exact.
- Use consistent units and significant digits within a table.
- Prefer formulas over long evaluated integers when the formula communicates
  the work more clearly.
- Define uncommon ratios and abbreviations at first use.

Use tables for repeated comparisons and figures for relationships that prose
cannot show efficiently. Use prose only to explain methodology,
interpretation, constraints, and decisions.

## Separate the design from the experiment record

Describe retained production mechanisms in the PR body. Keep rejected probes,
raw A/B tables, temporary instrumentation, profiler logs, and chronological
debug notes in working artifacts unless a compact comparison is essential to
justify a retained decision.

When listing optimizations, include only the few mechanisms that materially
explain the current design or result. Fold smaller refinements into the
implementation description.

Do not use candidate allocations, failed configurations, or hypothetical
limits as rows in a current resource-usage table.

## Report correctness without overclaiming

- State numerical or behavioral acceptance criteria before the results.
- Tie each result to its tested source and actual coverage.
- Keep different validation scopes distinguishable even when results share a
  table.
- Distinguish a production default from a diagnostic alternative.
- Do not infer full-gate approval from one favorable metric or one test case.
- Use a hidden TODO or an explicit open issue for required validation that is
  not yet complete; never write the desired result in advance.

## Handle figures and artifacts

- Generate figures from the source and measurements described by the PR.
- Distinguish direct samples, interpolation, derived series, and model-derived
  expectations in labels or captions.
- Do not relabel stale data as current.
- Preserve a clear HTML placeholder when a user will upload a pending figure.
- Keep local plots, CSVs, logs, and temporary scripts out of the production
  diff unless the repository explicitly requires them.

## Revise and publish

1. Audit the existing body for stale claims, duplicate explanations, patch
   notes, vague terminology, inconsistent scopes, and excess precision.
2. Draft the current design as a whole rather than editing one sentence at a
   time around obsolete structure.
3. Verify every headline, table, formula, link, source identity, test count,
   and figure caption against its evidence.
4. Confirm that Summary, Correctness, Performance, and integration evidence do
   not contradict one another.
5. Update the live PR only when the user authorized the mutation.
6. Re-read the live body after updating it. Confirm that rendering-sensitive
   Markdown, comments, tables, and links survived and that no concurrent
   content was lost.

## Final review

Before handing off the PR description, verify that:

- The opening states what the PR does and its supported boundary.
- Every section describes the current design rather than the edit history.
- Contracts, ownership, defaults, and unsupported cases are explicit.
- Correctness claims match their source, thresholds, and coverage.
- Performance claims state their boundary, denominator, and resources.
- Measured, derived, model-derived, and hypothetical values are distinguishable.
- Tables and figures carry the quantitative detail without repetitive prose.
- Significant digits match the evidence and decision.
- Rejected experiments and temporary artifacts are absent from the review
  narrative and production diff.
- The live PR body was re-read after publication.
