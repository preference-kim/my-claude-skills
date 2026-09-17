# PR description policy

## Language and publication

- Default to an English body with a summary written in Korean under
  `## Korean Summary` at the top. Present the initial manuscript and proposed
  language before publishing. Follow an explicit
  language request; do not reconfirm an approved choice.
- For a single-language body, use that language for headings and explanations,
  without a duplicate translation. Preserve established technical names, code,
  commands, and required GitHub closing syntax. Retain a labeled opening summary:
  `## Summary` in English or `## 요약` in Korean.
- Language approval does not approve an unseen manuscript. Existing approval of
  the concrete manuscript and language permits publication without another
  confirmation. Preserve the owning workflow's required review and write limits.

## Explain the change

- Write for the review decision. The opening summary connects the problem,
  retained solution, and concrete result, including material contracts and scope.
  It is not a word-count target or a list of implementation names. Avoid repeating
  the body; use subsections when they help the reader.
- Establish the component's behavior on the actual base. Explain what this PR
  changes, enables, and still leaves unavailable by itself. Include surrounding
  infrastructure only where it explains the change or an integration boundary.
  The title describes this PR's contribution, not a later stack layer's result.
- Name technical concepts directly and explain their execution relationship.
  For a changed component, connect where it is called, what changes and why,
  and the observed impact or missing comparison. Link the relevant code rather
  than replace a specific operation with an ambiguous label.
- Explain material output contracts through the producer-to-consumer path:
  contents, storage location, transfer or consumption, and lifetime. Identify
  allocation, ownership, borrowing or aliasing, and release responsibilities
  where they affect behavior. A class name or ownership adjective is insufficient.
- Attribute constraints to their source: semantics, preprocessing, feature scope,
  resources or concurrency, or deployment configuration. State the stage and units
  of size limits, including padding or alignment used for capacities. Do not
  describe an implementation capacity as a model limit or merge unrelated limits.

## Evidence and organization

- Make the body self-contained for review: include the final design, relevant
  contracts, reproduction procedure, and material results. Supporting references
  must not require the reviewer to reconstruct the argument elsewhere.
- Never include a local artifact path or cite a local-only file, log, plot, report,
  or working-tree state as evidence. Transfer material facts into the body. Chat,
  comments, dashboards, external documents, and unpublished artifacts cannot
  carry information needed to understand or validate the claim.
- Before reporting experiments, quantitative claims, correctness coverage,
  performance comparisons, or figures, read [evidence contracts](evidence.md).
  That reference owns reproducible commands, comparison tables, log excerpts,
  measurement scope, and figure readiness. Do not duplicate its requirements here.
- Prefer topic bullets with related explanations. Keep one coherent purpose per
  bullet and preserve causal connections; do not force every sentence into a list.
  Use headings for larger topics and deeper nesting only for necessary hierarchy.
  Remove repetition and generic background before removing definitions or evidence.
- Report change-specific correctness and performance evidence, material failures,
  missing checks, and limitations. Omit routine build-success statements and
  host-test counts; omit a validation section with no change-specific information.
  This controls reporting, not which required checks must run.

## Final-state scope

Describe the retained design and results relative to the base. Omit commit-by-commit
history, review iterations, rebases, intermediate candidates, superseded experiments,
transient regressions, retries, and rerun chronology. Keep the base behavior needed
to explain the change and direct performance comparisons needed to quantify it.
Do not narrate how the branch arrived at its final state.
