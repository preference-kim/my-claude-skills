# PR description policy

## Language and publication

Draft new or substantively revised descriptions in English with
[technical communication](../../technical-communication/SKILL.md), then prepare
the final language before independent technical prose and `stop-bullshit` review.
Translation preserves evidence, qualifications, and technical meaning. The English
working draft is not an extra delivered section.

Default to an English body preceded by `## Korean Summary` in Korean, which is
then the Summary section below; the English body does not repeat it. A requested
single-language body uses that language for prose, with `## Summary` and no
duplicate translation. Before choosing, read the
[team writing policy](../../../agent-guidance/team-development.md); it can set
another default for the repositories it covers. An explicit request for the PR
overrides any default. Write Korean prose in 개조식 or 하다체. The AGENTS.md
Language section governs English titles, headings, terms, and table and figure
text. Keep the title to about 60 characters, naming the main contribution.
Preserve code, commands, and GitHub closing syntax.

For the user's own PR, publish a new or revised description body after the
required review and your final check without waiting for approval. Read it back,
then ask the user to review it and state what changed. Revise and publish a stale
description of the user's unmerged PR the same way, whether a push, a lower PR's
merge, a rebase, or new evidence made it stale; the push itself follows the
[Git policy](../../../agent-guidance/version-control.md#pr-branch-synchronization).
Changing an existing PR's title still needs the user's approval. For another
author's PR, publish only a reviewed manuscript the user approved.

## Structure the description

The description alone must let a reviewer understand the situation, the intent,
the analysis behind the change, and its rationale. A PR comment or linked page
can supplement it but cannot carry what the review decision needs.

Carry the flow of these sections in bullets; use a short paragraph only for
context a bullet cannot hold:

- **Summary:** three titled bullets (problem, change, result), titled in the
  Summary's language and each at most two sentences. The problem bullet gives the
  background problem and the goal, the change bullet the core change, and the
  result bullet the outcome within this PR's scope: an optimization's speedup, or
  for a bug fix, briefly what was fixed and how. Keep the qualifier that bounds
  each claim, such as its condition or whether it was measured or derived from
  code. Leave revisions, runs, and which commit passed which check to the owning
  section.
- **Change chapters:** one or more chapters explain the changes, each headed for
  the change it explains. For each, state how Base behaves, what this PR changes,
  and why. Give changes of different kinds, such as a feature, an interim
  workaround, and a bug fix found during the work, separate chapters. A one-line
  fix needs one short chapter.
- **Other changes:** one brief `## Other changes` section lists changes outside
  the main issue, each with its reason. Omit it when there are none.
- **Evidence:** results and validation sections, headed for their content, hold
  what the review decision needs.

When the repository spans several software layers or components, name the layer
of each background item and change, using the layer names the repository's
documentation defines, or the component's established name where none is
defined. When the change depends on runtime structure, such as process
boundaries, call order, or a pipeline schedule, explain that structure plainly
before the mechanism, with a small text diagram where timing matters. When a rule treats cases differently,
list each case and why it needs separate handling. When shared code changes, list
which of its other users change behavior. Consider a diagram or plot where it
explains a change or result better than text or a table, attached as a linked
supplementary figure when the body cannot render it; the
[evidence contracts](evidence.md) govern figures.

Plan the reader's decision before drafting: what behavior or contract changes,
what evidence supports it, and what remains unresolved. Select the facts needed
for that decision before adding implementation detail. A description is not an
inventory of the work performed. Keep detailed contracts, methods, and numerical
results in their owning sections instead of repeating them in the Summary and
body. Describe the actual base-to-head change, not a later stack layer's outcome
or branch development history. Include surrounding infrastructure only when it
explains behavior or an integration boundary.

## Explain the retained change

Use established codebase terms and connect the changed component's callers,
behavior, mechanism, and observed impact or missing comparison. Where material,
put the changed interface in the visible body: inputs/outputs, defaults, and
whether calls return new storage or mutate caller-provided buffers. Include
shapes, invariants, unsupported cases, and synchronization when they affect use.

For a new or changed callable interface, show its public signature in a fenced
code block with the appropriate language. Use the caller-facing API from the
inspected binding or declaration, including arguments, defaults, and return type
where declared. Explain material return behavior separately when the signature
does not express it. Identify the API layer when several signatures exist.
For tensor operations, document the call contract as well as the signature.
For each new or changed tensor, state its role, shape, dtype, element layout,
buffer type, and device memory layout or sharding. Distinguish device storage
from placement across devices. Cover returned and caller-provided output tensors,
including mutation and aliasing rules. A new op needs its full interface; an op
revision may focus on changed arguments, outputs, and constraints, retaining
unchanged facts only when needed to use the change. Shared constraints can appear
once above a compact parameter table; do not impose this table on unrelated PRs.

Separate required and supported configurations, defaults, and recommendations.
Give relevant memory, program, and compute configuration values with their
hardware/workload conditions and the source or measurement supporting the
recommendation. A configuration fixed by the implementation is a requirement,
not a tuning recommendation. Identify a supported allocation helper when useful;
do not invent configurable options or a recommended value without evidence.
Check bindings, validation, implementation, and relevant callers/tests for these
claims. State material documentation/implementation discrepancies or missing
recommendation evidence explicitly.

For relevant data paths, explain the overall behavior before inventorying fields.
A reader must be able to follow the trigger and inputs through the material
processing stages to outputs and their later consumers. Explain why each material
data item is needed, who produces and consumes it, and whether it is a supplied
input, derived result, retained state, or output at each boundary. Connect storage,
transfer, lifetime, allocation, ownership, aliasing, and release to that flow.
When an algorithm or protocol determines the interface, give the short mechanism
needed to understand those relationships. Distinguish semantic requirements from
the current representation; a stored field's existence alone does not justify its
necessity. Inspect missing links or state them as unresolved rather than inventing
a rationale. Attribute constraints to semantics,
preprocessing, feature scope, resources/concurrency, or deployment. Give size-limit
stages, units, padding, and alignment. Distinguish implementation capacity from
model limits.

Within that structure, cover only the topics the change needs: contracts,
implementation, correctness, performance, resources, integration, or remaining
limits. Use further hierarchy only when useful. The reader must understand the
base-to-PR change and source of each material constraint without reconstructing
the argument from names or links.

Label the base and this PR "Base" and "This PR" in text and tables, and define
each once with its revision and what it contains; a revision hash alone does not
tell the reader which side it is. Name other implementations or comparisons by
API, algorithm, or distinguishing configuration. Relative adjectives such as
"ordinary", "optimized", or "new" cannot identify a comparison on their own. Do
not invent abbreviations or slash-packed metrics to make a table fit. When
scenarios change the operation, workload, or outcome being measured, use separate
subsections or tables if a combined table requires decoding a legend.
Established technical abbreviations remain appropriate for their audience.

## Evidence and presentation

In PR tables, keep one row per distinct case. Collapse duplicate rows and
repeated runs of the same case, including rows that differ only by repeat index.
For repeated measurements, state the repeat count and aggregation method with
the retained result; preserve material variation or failures in that row or its
adjacent explanation. Keep cases with materially different conditions separate.

Keep the visible body within 7,000 characters, including the summary, headings,
tables, and visible `<summary>` labels. Count Unicode code points (Python `len`
of the decoded text) after removing
the hidden contents of collapsed `<details>` blocks; count the remaining Markdown
including whitespace as a conservative bound. Check the final saved manuscript,
not an earlier draft, with a deterministic count rather than an estimate. If
counting is unavailable, report compliance as unverified. The limit exists to
refine the content into what a reviewer can take in; it is a ceiling, not a
target. Above it, first cut repetition and detail the review decision does not
need, and move secondary detail into collapsed blocks. If the core of the PR
still cannot be conveyed clearly within the limit, exceed it by what the core
needs and report the final count with the reason; conveying the information is
the governing principle. Never compress sentences or drop the core to fit.

Keep the changed contract, measurement method, main results, and limitations
needed for the review decision visible. Use compact bullets for experimental
setup. Put derivations, secondary cases, full commands, and detailed evidence in
labeled collapsed blocks. Remove repetition and irrelevant detail before moving
text there; hidden content also needs an explicit reader purpose. Do not meet the
budget by hiding a material limitation, omitting the contract, or compressing
names into unexplained shorthand.

Keep the design, contracts, reproduction, and material results self-contained
across the description and its collapsed blocks.
Supporting links cannot replace decision-critical facts. Do not include
local artifact paths or cite local-only files, logs, figures, or working-tree state
as evidence.

For experiments, quantitative claims, correctness coverage, performance comparisons,
or figures, read [evidence contracts](evidence.md) before reporting them.
Report change-specific results, failures, missing checks, and limitations. Omit
routine build-success statements, host-test counts, and empty validation sections.
This reporting rule does not waive required checks.

Use words for approximations and words or an en dash for ranges. Bare `~` can pair
across a GitHub body and strike through unrelated text. Escape literal tildes as
`\~` or use code spans. Preserve tildes in code, URLs, and intentional strikethrough.
If any remain, check the complete body with GitHub Preview or its Markdown API.
Raw Markdown readback does not verify rendering.

Report retained design and final results relative to the base. Keep relevant
baselines and comparable performance conditions. Omit superseded candidates,
transient failures, review/rebase history, retries, and rerun chronology.

Before manuscript review, reconstruct the changed behavior from the document
without filling gaps from the conversation or unstated code knowledge. Check that
the visible body explains the changed contract, material data relationships and
results. Completion means the reader can understand the whole relevant flow and
why its data is needed, not merely find every requested heading or field. Scale
this check to the change; it requires no sections beyond those above, and no
diagram or algorithm tutorial. This check supplements the language, contract, and evidence
requirements; it does not replace them. Missing links need source inspection or
an explicit gap.
