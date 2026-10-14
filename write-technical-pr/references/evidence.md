# PR evidence contracts

## Scope each claim

Distinguish direct measurements, calculations from measured inputs, model-derived
estimates, hypotheses awaiting a test, and design decisions justified by criteria.
Do not label derived values as measured. Give the source revision's role and its
relationship to PR head, workload, units, denominator, resources, and protocol
needed to interpret a claim. Qualify stale or narrower evidence beside the claim,
or omit it. Candidate allocations are not current resource usage.

For comparisons, name the baseline, changed code/option, and conditions held equal.
Final latency alone does not establish speedup. If the baseline was not measured,
state that gap without inventing its cause or implying no benefit. Narrow the claim
unless the task requires the missing experiment. Description writing alone does
not authorize experiments or implementation changes.

For performance results, place a compact method description beside the tables:
the repository script/test entry point; clock source and timed boundary (for
example, device timestamps or host wall time around trace replay); profiler
state; repetitions, aggregation, and whether inputs/randomness vary. State the
hardware, workload, and configuration differences that affect comparability.
Keep full commands and setup in a collapsed reproduction block. A unit such as
microseconds does not identify what was timed.

Distinguish per-call statistics from averages over repeated calls and aggregates
of those averages. For data-dependent work, explain what variation the reported
samples cover. Fixed-input replay does not establish a workload latency
percentile. Report available tail/iteration statistics when they bear on the
claim, or state the missing coverage without inventing values or starting an
unrequested experiment.

## Quantitative results

Keep system-level achievement against a stated target model separate from
component utilization against theoretical peak:

- Define the measured system boundary and target before reporting achievement,
  including the model's compute, communication, and memory assumptions.
- For components, use the peak of the participating cores, links, banks, or devices.
  State their counts and use operation-weighted peaks for mixed operations.
  Define useful payload and directionality for bandwidth. Leave utilization blank
  without a defensible peak and work count.
- Treat overlapping intervals as intervals, not additive latency. Use distinct
  columns for target-model achievement and theoretical-peak utilization.

Preserve precision needed for acceptance thresholds, reproducibility, and close
comparisons. Keep contractual constants, shapes, and byte counts exact. Otherwise
round consistently, use clear units and significant digits, define uncommon ratios,
and prefer a formula when it communicates work better than a long integer.

## Reproduction and coverage

For every reported experiment, include its exact command in a fenced `bash` block:
repository-relative working directory, required environment and inputs, and exact
test/benchmark selection. The procedure must work without local aliases, private
wrappers, undeclared state, or machine-specific absolute paths. A simplified
procedure is a verified reproducer only if that version was checked.

Put results and their method, conditions, units, and acceptance/comparison basis
together within the description policy's visible-body budget. Use tables for
comparable results and avoid repeating the same values elsewhere. Give numerical
or behavioral acceptance criteria before results and
tie each result to its actual tested source and coverage. Distinguish validation
scopes and production defaults from diagnostic alternatives. One passing metric
or case does not establish full-gate approval. Mark unfinished required validation
with an explicit open issue or hidden TODO, not a predicted result.

When logs establish a result or failure, include the relevant excerpt in a fenced
block and explain it. Put detailed excerpts in a labeled
`<details><summary>...</summary>...</details>` block. Exclude unrelated output,
secrets, and local paths.

## Figures and artifacts

Use a figure when a table does not communicate the relationship well. Generate it
from the described source and measurements. Label samples, interpolation,
derived series, and modeled expectations distinctly. Required figures must be
attached before publication, replaced by complete tables, or their claims omitted.
Do not relabel stale data as current.

Keep local plots, CSVs, logs, and temporary scripts out of the production diff
unless the repository requires them. The [description policy](policy.md)'s
self-contained evidence and citation requirements apply to figures too.
