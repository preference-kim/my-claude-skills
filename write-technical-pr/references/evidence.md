# PR evidence contracts

## Reuse completed validation

When deciding whether PR validation needs more work, read the
[PR validation rule](../../../agent-guidance/version-control.md#pr-validation).
It owns the cost and purpose of additional checks and reuse after history changes.

For Base-versus-This-PR measurements, identify each side by its role and actual
tested revision. This PR names the change being evaluated, not a promise that the
measurement ran at the current head. Preserve the actual measured hashes after
a rebase or force-push; never replace them with unmeasured revisions. A revision
change alone warrants neither a stale-evidence warning nor a rebase explanation.
Keep routine author checks and rerun inventories out of the description. Report
a material remaining defect or evidence gap in terms of the affected behavior
and claim, without narrating branch history.

## Scope each claim

Distinguish direct measurements, calculations from measured inputs, model-derived
estimates, hypotheses awaiting a test, and design decisions justified by criteria.
Do not label derived values as measured. Give source revisions and their
comparison roles, workload, units, denominator, resources, and protocol where
needed to interpret a claim. For measurements, use the actual tested revisions.
Qualify evidence whose tested behavior or conditions support only a narrower claim
in its owning section; replace or omit evidence
that no longer supports it. Candidate allocations are not current resource
usage. Report the configurations the review decision needs or the user named.

For comparisons, name the baseline, changed code/option, and conditions held equal.
State an optimization's speedup as a ratio above one: Base ÷ This PR for a time,
This PR ÷ Base for a rate such as throughput. Give the direction of any other
ratio, such as a longer latency. Final latency alone does not establish speedup.
If the baseline was not measured, state that gap without inventing its cause or
implying no benefit. Narrow the claim unless the task requires the missing
experiment. Description writing alone does not authorize experiments or
implementation changes.

Beside performance results, identify the clock and the timed boundaries, such as
host wall time around trace replay. State profiler status, repetitions,
aggregation, and whether inputs or randomness varied. Name the hardware,
workload, and configuration differences that affect comparability.

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

For each experiment, briefly state the question it answers, the conditions being
compared, the values to observe, and when in execution to observe them. Give
enough detail for a reader to implement the measurement independently. Cite a
shared test or workload when it identifies the setup. Include a short command
when its options determine the measurement or the user requests it. Describe a
procedure as verified only if that procedure was run.

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

Generate a figure from the described source and measurements. Label samples,
interpolation, derived series, and modeled expectations distinctly. Before
publication, attach a figure that carries a claim to the description, replace it
with complete tables, or omit its claim. A linked figure, such as one on a host
the team writing policy approves, only supplements text or tables that carry the
claim. Preserve the measured revisions and coverage in figures as in tables.

Keep local plots, CSVs, logs, and temporary scripts out of the production diff
unless the repository requires them. The [description policy](policy.md)'s
self-contained evidence and citation requirements apply to figures too.
