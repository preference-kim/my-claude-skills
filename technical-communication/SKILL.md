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

Lead with the supported conclusion and its scope. An issue or defect report states
in its title and opening the consequence (error, wrong output, or cost), whether
correctness is affected, and its size or that it is unmeasured; a report that asks
for a change also states the goal and where the change must happen. Connect the
material conditions, inputs, mechanism, and outputs so the reader can follow why
the result occurs. Identify the exact object under discussion: the callable and
its contract, or the script, revision, invocation, and configuration behind a
result. Give the concrete signature or command when it determines use or
reproduction; a descriptive name or link alone is insufficient. Include ownership, state changes, failure paths,
or tradeoffs when they affect use or the decision. Explain consequential
constraints rather than merely naming fields or listing implementation steps.

Use established technical terms consistently. Define an unfamiliar term for this
audience by what it contains or excludes; do not replace precise terms with broader
everyday words. Preserve distinctions such as verification against a specification
and validation for an intended use when the work makes them. Keep the text and
each sentence as short as a precise account of the intent and mechanism allows;
shorten syntax, not meaning. Use paragraphs or bullets for the flow, lists for
parallel items, and tables for comparisons. When table cells would hold sentences,
first consider bullets instead. Bold the title of a titled bullet. Follow the
structure the artifact's owning contract defines; otherwise add no template,
rhetorical introduction, or sentence-length quota.

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
without inventing precision, missing samples, or general guarantees. Before a
results table, state what was measured and what a difference between cases
isolates, define the entities involved, and describe each scenario by its system
state. Label a case by what was measured, not by an outcome it does not represent.

## Revise as a whole

Interpret feedback against the original objective and accepted constraints.
Determine which claim or behavior it changes, then update dependent conclusions
in their owning sections. Replace stale text. Do not append a correction while
leaving the contradicted claim elsewhere, or turn one local comment into the
document's new purpose. Preserve concurrent content and requirements still in
force; inspect material ambiguity before changing scope.

The artifact itself must let its reader understand the situation and the
intent; linked comments or pages supplement it but cannot carry what the
reader's purpose needs. A length limit exists to refine content into what that
reader can take in. When the core still cannot be conveyed clearly within a
limit after cutting what the purpose does not need, extend the text where the
owning contract allows it, or report what a fixed limit cuts; do not drop or
compress the core. Attach a diagram as supplementary material when it conveys
structure or timing better than prose and the artifact cannot hold it.

Remove repetition, embellishment, incidental history, defensive caveats,
disclaimers that bound no claim, and sentences that leave the document's point
before removing useful conditions or evidence. Keep an earlier attempt only
when it explains a decision, risk, or reproduction step. Report execution,
observed results, and acceptance separately when their distinction matters.

After the last edit, check each sentence skeptically: whether its logic holds,
whether it follows from the previous sentence and leads to the next, and whether
an expression admits more than one reading. Replace such an expression with one
that admits only the intended reading. Then reconstruct the argument from the
saved artifact without the conversation: can this reader explain the result, its
basis, its limits, and the required next action? Repair gaps and stop when the
purpose is met.
Use `stop-bullshit` when an explicit audit or the owning workflow requires it;
ordinary editing does not require an audit report.

## Conditional references

Before introducing or assessing a technique or concept name, including one taken
from code, read [domain research](../../agent-guidance/domain-research.md). Verify
the semantic fit before building an explanation around it; reuse sufficient prior
research. This reference also applies when this skill is loaded in isolation.

When a private team policy is registered, read its writing policy through the
[team policy loader](../../agent-guidance/team-development.md) before writing;
that policy defines which work it covers. An isolated reviewer uses the policy
sections and revision its brief supplies instead of running the loader.

For an explicit STE compliance request, inspect the requested edition of the
standard and the pinned [SimpleEnglish reference](../simple-english/skills/simple-english/SKILL.md).
Do not infer compliance from the skill's branding or apply word substitutions
that change meaning. For deliberate maintenance of this skill, consult selected
rules or examples from SimpleEnglish or [humanizer](../humanizer/SKILL.md) and
test the proposed change. Neither reference is a routine writing pass.
