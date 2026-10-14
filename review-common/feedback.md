# PR finding contract

Retain one concrete, high-confidence issue per finding. Establish the triggering
conditions, observed behavior or violated invariant, and impact. Explain the
contract the fix must satisfy, then give a specific code or test suggestion.
Cite the smallest relevant changed location and any applicable authoritative
reference, explaining why it applies. The comment must carry the causal argument
without making the reader reconstruct it from links.

Before judging a changed interface or data flow, trace the relevant behavior
across its callers and stages. Establish what each material value represents, why
it is needed, and how its role or ownership changes from production to later use.
Distinguish algorithm or protocol requirements from choices in the current
representation. If a relationship is unclear, locate the ambiguity and explain
its concrete effect on implementation, use, or maintenance; the presence of fields
or documentation alone does not establish a coherent contract. Do not turn a
preferred presentation into a correctness finding.

Prioritize correctness, concurrency, security, compatibility, resource lifetime,
test coverage, and material maintainability in changed behavior. Use surrounding
code to establish impact. Exclude speculative and style-only findings.
A no-finding result is valid. Preserve material uncertainty and required reviewer
prefixes. Use connected prose without a mandatory three-part template or generic
background.

Before preparing isolated leaf prompts, read
[stop-bullshit](../stop-bullshit/SKILL.md). Supply this contract, the applicable
reasoning and communication principles from canonical AGENTS.md, and that skill's
loaded instructions. Provide contents if canonical files are inaccessible.
Leaves apply the check directly, without another critic or orchestration skill.
Check both the reviewed material and comments before any permitted write.
The orchestrator also applies this contract and the final substance check when
consolidating all reviewers' findings and after the last prose edit.
