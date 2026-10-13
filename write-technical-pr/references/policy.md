# PR description policy

## Language and publication

Draft new or substantively revised descriptions in English with
[SimpleEnglish](../../simple-english/skills/simple-english/SKILL.md), then prepare
the final language before independent `humanizer` and `stop-bullshit` review.
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

The opening summary connects the problem, solution, and concrete result within
this PR's scope. Describe the actual base-to-head change, not a later stack layer's
outcome or branch development history. Include surrounding infrastructure only
when it explains behavior or an integration boundary.

Use established codebase terms and connect the changed component's callers,
behavior, mechanism, and observed impact or missing comparison. Where material,
state changed inputs/outputs, shapes, invariants, defaults, unsupported cases,
and synchronization. For relevant data paths, trace outputs from producer to
consumer: contents, storage, transfer, lifetime,
allocation, ownership, aliasing, and release. Attribute constraints to semantics,
preprocessing, feature scope, resources/concurrency, or deployment. Give size-limit
stages, units, padding, and alignment. Distinguish implementation capacity from
model limits.

Choose topics the change needs: contracts, implementation, correctness,
performance, resources, integration, or remaining limits. Prefer coherent topic
bullets with related explanations. Use further hierarchy only when useful.
The reader must understand the base-to-PR change and source of each material
constraint without reconstructing the argument from names or links.

## Evidence and presentation

Keep the design, contracts, reproduction, and material results self-contained.
Supporting links cannot replace decision-critical facts in the body. Do not include
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
