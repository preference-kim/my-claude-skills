# PR description policy

## Language and publication

Draft new or substantively revised descriptions in English with
[technical communication](../../technical-communication/SKILL.md), then prepare
the final language before independent technical prose and `stop-bullshit` review.
Translation preserves evidence, qualifications, and technical meaning. The English
working draft is not an extra delivered section.

Default to an English body preceded by `## Korean Summary` in Korean. A requested
single-language body uses that language for prose, with `## Summary` and no duplicate
translation. PR titles, headings, conventional technical terminology, and all text
in tables, plots, and figures remain English, even for an entirely Korean request.
Preserve code, commands, and GitHub closing syntax.

Present the initial manuscript and proposed language before publication. Explicit
language instructions settle that choice, but do not approve an unseen manuscript.
Existing approval of the concrete manuscript and language permits publication
without reconfirmation, subject to the owning workflow's review and write limits.

## Explain the retained change

Plan the reader's decision before drafting: what behavior or contract changes,
what evidence supports it, and what remains unresolved. Select the facts needed
for that decision before adding implementation detail. A description is not an
inventory of the work performed. Use the summary for the purpose and result;
keep detailed contracts, methods, and numerical results in their owning sections
instead of repeating them in the summary and body.

The opening summary connects the problem, solution, and concrete result within
this PR's scope. Describe the actual base-to-head change, not a later stack layer's
outcome or branch development history. Include surrounding infrastructure only
when it explains behavior or an integration boundary.

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

Choose topics the change needs: contracts, implementation, correctness,
performance, resources, integration, or remaining limits. Prefer coherent topic
bullets with related explanations. Use further hierarchy only when useful.
The reader must understand the base-to-PR change and source of each material
constraint without reconstructing the argument from names or links.

Name each implementation or comparison by its branch/revision, API, algorithm,
or distinguishing configuration. Relative adjectives such as "ordinary",
"optimized", or "new" cannot identify a comparison on their own. Do not invent
abbreviations or slash-packed metrics to make a table fit. When scenarios change
the operation, workload, or outcome being measured, explain each scenario briefly
and use separate subsections/tables if a combined table requires decoding a legend.
Established technical abbreviations remain appropriate for their audience.

## Evidence and presentation

Keep the visible body within 7,000 characters, including the summary, headings,
tables, and visible `<summary>` labels. Count Unicode code points (Python `len`
of the decoded text) after removing
the hidden contents of collapsed `<details>` blocks; count the remaining Markdown
including whitespace as a conservative bound. Check the final saved manuscript,
not an earlier draft, with a deterministic count rather than an estimate. If
counting is unavailable, report compliance as unverified. This is a ceiling, not
a target. An over-budget manuscript remains a draft until it is reduced.

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
this check to the change; it does not require a fixed template, diagram, or
algorithm tutorial. This check supplements the language, contract, and evidence
requirements; it does not replace them. Missing links need source inspection or
an explicit gap.
