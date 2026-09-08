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

Explain a source revision's role and relationship to the submitted implementation;
a bare hash is not measurement context. For an optimization comparison, name the
baseline, the changed option or code, and the conditions held equal instead of
using an unexplained qualifier such as "matched." Distinguish final latency from
speedup. When only the final path was measured, identify the missing baseline;
do not invent a reason it was omitted or imply that no benefit exists.
Unless the task requires that comparison, narrow the performance claim rather
than turn missing measurements into a new experiment or publication prerequisite.

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
