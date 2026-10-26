---
name: technical-communication
description: Use to write, revise, or assess technical documents and substantial engineering explanations or result reports. Preserve meaning, evidence, and the reader's decision. Not for ordinary short replies, standalone style polishing, or auditing the agent's conduct; PR and handoff workflows retain their own contracts.
---

# Technical communication

Help the intended reader understand, decide, reproduce, or continue the work.
Read the relevant sources and existing artifact before writing. Establish the
reader, purpose, requested change, and facts needed for that purpose. Apply an
artifact's owning contract, such as PR evidence or handoff contents; this skill
does not authorize experiments, publication, or changes beyond the request.

## Explain the work

Lead with the supported conclusion and its scope. Connect the material conditions,
inputs, mechanism, and outputs so the reader can follow why the result occurs.
Identify the exact object under discussion: the callable and its contract, or the
script, revision, invocation, and configuration behind a result. Give the concrete
signature or command when it determines use or reproduction; a descriptive name
or link alone is insufficient. Include ownership, state changes, failure paths,
or tradeoffs when they affect use or the decision. Explain consequential
constraints rather than merely naming fields or listing implementation steps.

Use established technical terms consistently. Define unfamiliar terms for this
audience; do not replace precise terms with broader everyday words. Preserve
distinctions such as verification against a specification and validation for an
intended use when the work makes them. Shorten syntax without shortening meaning.
Use connected paragraphs, lists for parallel items, and tables for comparisons.
Do not impose a template, rhetorical introduction, or sentence-length quota.

## Match claims to evidence

Distinguish observations and measurements from assumptions, hypotheses, and
inferences. State the conditions and premises needed to interpret a claim.
Preserve justified uncertainty, including modal words when they express it;
remove an unsupported assertion rather than disguising it with a hedge.
Explain plausible alternatives only when they could change the conclusion or
next action, and identify the evidence that would distinguish them.

Attach the smallest relevant inspected source to the claim it supports. Keep
decision-critical facts and reasoning in the artifact. For an external reader,
include accessible source revisions and reproducible commands or code instead
of local-only evidence. Same-environment reports may link local files but must
carry the conclusion and essential context. Distinguish a proposed procedure
from one actually run; a simplified reproducer is verified only after that
version was checked. Report measurements with comparable conditions and scope,
without inventing precision, missing samples, or general guarantees.

## Revise as a whole

Interpret feedback against the original objective and accepted constraints.
Determine which claim or behavior it changes, then update dependent conclusions
in their owning sections. Replace stale text. Do not append a correction while
leaving the contradicted claim elsewhere, or turn one local comment into the
document's new purpose. Preserve concurrent content and requirements still in
force; inspect material ambiguity before changing scope.

Remove repetition, embellishment, incidental history, and defensive caveats
before removing useful conditions or evidence. Keep an earlier attempt only
when it explains a decision, risk, or reproduction step. Report execution,
observed results, and acceptance separately when their distinction matters.

After the last edit, reconstruct the argument from the saved artifact without
the conversation: can this reader explain the result, its basis, its limits,
and the required next action? Repair gaps and stop when the purpose is met.
Use `stop-bullshit` when an explicit audit or the owning workflow requires it;
ordinary editing does not require an audit report.

## Conditional references

Before introducing or assessing a technique or concept name, including one taken
from code, read [domain research](../../agent-guidance/domain-research.md). Verify
the semantic fit before building an explanation around it; reuse sufficient prior
research. This reference also applies when this skill is loaded in isolation.

For an explicit STE compliance request, inspect the requested edition of the
standard and the pinned [SimpleEnglish reference](../simple-english/skills/simple-english/SKILL.md).
Do not infer compliance from the skill's branding or apply word substitutions
that change meaning. For deliberate maintenance of this skill, consult selected
rules or examples from SimpleEnglish or [humanizer](../humanizer/SKILL.md) and
test the proposed change. Neither reference is a routine writing pass.
