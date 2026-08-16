---
name: write-technical-pr
description: Draft, restructure, audit, and update technical GitHub pull-request descriptions as concise, self-contained current-design documents. Use when creating or revising a PR body, especially for systems, kernel, distributed, performance, or model-integration work that must explain interfaces, invariants, implementation, correctness, resource limits, reproducible benchmarks, figures, and remaining constraints.
---

# Write Technical PR

Write the PR description as a decision document for reviewers. Present the
current change, its evidence, and its limits as one self-contained argument.
Do not turn the PR body into an experiment log or edit history.

## Write only the final state and final results

Write as though the final branch appeared in its current form. State the final
retained design, its behavior relative to the base branch, final validation
outcomes, final measurements, and remaining constraints. Do not narrate how the
branch reached that state.

Exclude commit-by-commit evolution, review iterations, rebases, remote-branch
updates, intermediate candidates, superseded maps or allocations, failed or
discarded experiments, transient regressions, fixes to problems absent from the
final change, infrastructure retries, and rerun chronology. Avoid narrative
labels such as "initial", "follow-up", "candidate", "final candidate",
"previously", "then", and "later" when they describe branch history rather
than the resulting design.

A historical baseline may appear only as a direct side-by-side comparison
needed to quantify or justify a retained final result. Present the baseline,
final value, workload, and delta together; do not explain the sequence of
experiments that produced them. A commit SHA may identify measurement source,
but must not become a development timeline. If evidence was not measured at
the PR head, give the narrow evidence-scope qualifier adjacent to the claim or
omit the claim; do not narrate why successive reruns did or did not occur.

## Keep the review self-contained

- Include every material fact needed to understand the problem, retained
  design, relevant contracts and constraints, reproduction procedure, and
  evidence in the PR description itself.
- Never include a local artifact path or cite a local-only file, log, plot,
  report, working-tree state, or other reviewer-inaccessible resource as
  evidence. Transfer its material facts into the PR body.
- Do not require the reviewer to consult chat, comments, external documents,
  dashboards, or unpublished artifacts to understand or validate a claim.
  External references may provide supplementary detail only.
- Use direct, specific wording. Write short bullets grouped by distinct topics
  instead of dense paragraphs, ambiguous abstractions, or repetitive prose.

## Establish the review scope

1. Identify the repository, PR, base, head, audience, and decision the reviewer
   must make.
2. Inspect the actual diff and the source, design documents, tests, benchmark
   artifacts, and integration reports needed to verify the claims.
3. Separate retained and validated behavior from work in progress, rejected
   probes, historical baselines, transient bugs or errors resolved during
   development, and unverified plans. Omit the non-final material. When a
   retained decision needs evidence, state the final constraint and the direct
   matched comparison without recounting the branch history.
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

- **Korean Summary:** Make `## Korean Summary` the first section. Write it in
  Korean using vocabulary and concepts already established in the codebase.
  State the core problem, retained solution, and concrete result without
  external context or unexplained promotional terminology.
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

Present concrete results in Markdown tables. Include the workload, conditions,
units, acceptance criterion or comparison basis, and result needed to interpret
each value. Use figures only for relationships that a table cannot show
efficiently. Use short bullets only to explain methodology, interpretation,
constraints, and decisions.

## Make experiments reproducible

- For every reported experiment, provide the exact command line in a fenced
  `bash` code block.
- Include the repository-relative working directory, required environment
  variables and inputs, and exact test or benchmark selection.
- Do not depend on local aliases, private wrappers, undeclared state, or
  machine-specific absolute paths.
- Put concrete results in the corresponding Markdown table, not only in prose
  or an external artifact.
- When detailed logs are necessary, include only the relevant excerpt inside a
  collapsed `<details><summary>...</summary>...</details>` block with a
  specific summary label. Omit irrelevant output, secrets, and local paths.

## Separate the design from the experiment record

Describe retained production mechanisms in the PR body. Omit rejected probes,
raw A/B tables, temporary instrumentation, profiler logs, and chronological
debug notes. Do not link to their local artifacts. When a compact comparison
is essential to justify a retained decision, show only the baseline and final
result under the matched protocol.

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
- Do not hand off a PR that depends on a pending figure. Attach a required
  figure or replace it with a complete table before publication; otherwise
  omit the unsupported claim.
- Keep local plots, CSVs, logs, and temporary scripts out of the production
  diff unless the repository explicitly requires them.
- Never expose their local paths or require them to interpret the PR. Put the
  necessary values, method, and conclusion in the PR body.

## Revise and publish

1. Audit the existing body for stale claims, duplicate explanations, patch
   notes, vague terminology, inconsistent scopes, and excess precision.
2. Draft the current design as a whole rather than editing one sentence at a
   time around obsolete structure.
3. Verify every headline, table, formula, link, source identity, test count,
   and figure caption against its evidence.
4. Confirm that Korean Summary, Correctness, Performance, and integration
   evidence do not contradict one another.
5. Update the live PR only when the user authorized the mutation.
6. Re-read the live body after updating it. Confirm that rendering-sensitive
   Markdown, comments, tables, and links survived and that no concurrent
   content was lost.

## Final review

Before handing off the PR description, verify that:

- `## Korean Summary` is the first section and states the core problem,
  retained solution, and concrete result using established codebase terms.
- The PR body contains every material fact needed for the review decision and
  does not cite local artifacts or require external context.
- Text uses short, topic-grouped bullets with direct and specific wording.
- Every section describes the current design rather than the edit history.
- No section tells the story of how the branch evolved; comparisons contain
  only the baseline and final result needed for the review decision.
- Contracts, ownership, defaults, and unsupported cases are explicit.
- Correctness claims match their source, thresholds, and coverage.
- Performance claims state their boundary, denominator, and resources.
- Measured, derived, model-derived, and hypothetical values are distinguishable.
- Tables and figures carry the quantitative detail without repetitive prose.
- Significant digits match the evidence and decision.
- Rejected experiments and temporary artifacts are absent from the review
  narrative and production diff.
- Every reported experiment has an exact reproducible command in a fenced
  `bash` block and its concrete results in a Markdown table.
- Necessary detailed logs are reduced to relevant excerpts in collapsed
  `<details>` blocks; secrets and local paths are absent.
- The live PR body was re-read after publication.
