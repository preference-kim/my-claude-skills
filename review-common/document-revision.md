# Document revision workflow

Use this workflow for handoffs and PR descriptions. Complete a separate-agent
review and the resulting revision pass before calling the document final.

## Give the reviewer the draft and its basis

Prepare a complete draft under the owning document policy. Read
[humanizer](../humanizer/SKILL.md) and [stop-bullshit](../stop-bullshit/SKILL.md)
before composing the review brief. Start a separate agent with:

- The exact draft or versioned file, its purpose, audience, requested language,
  user requirements, and existing publication authority.
- The relevant source material and evidence, with claim-specific pointers and
  explicit gaps. Include the handoff's opening prompt when reviewing a handoff;
  include the base/head diff and evidence for claims retained in a PR description.
- The applicable reasoning and communication principles from the canonical
  AGENTS.md, plus the owning handoff content contract or PR description policy
  and applicable evidence contracts. Read them before preparing the brief.
  Supply their contents when the reviewer cannot access the canonical files;
  carry required conditional rules into the isolated context as well.
- Readable canonical paths to both skills above, or their full loaded instructions
  when isolated. Naming skills without supplying access to them is insufficient.

Use only sources authorized for the reviewer's environment. Keep internal drafts
and evidence within their permitted storage and audience.

## Reviewer contract

The reviewer inspects the draft and relevant sources independently. It applies
`humanizer` in embedded mode to improve the prose while preserving the required
structure, technical meaning, and uncertainty. It then applies `stop-bullshit`
after the prose pass, checking both the proposed document and its own feedback.
Style improvements must not invent facts or preserve a contradicted claim merely
because it appeared in the source draft.

Check whether a reader without the conversation can follow each material
conclusion and access its support. Distinguish an explanation missing from the
draft from a fact missing in the evidence; editing cannot supply the latter.
Return material findings with their evidence and precise locations, proposed
revisions, and any unresolved source or scope gap. A no-finding result is valid;
do not manufacture changes to demonstrate activity. Identify which draft was
reviewed and any portion that could not be checked.

The reviewer is a read-only leaf: it may propose replacement text but must not
overwrite the shared draft, modify implementation or evidence, publish, contact
others, invoke a review-orchestration skill, or spawn another reviewer. The
authoring agent owns revision and delivery.

## Resolve and finalize

Evaluate each finding against the task and sources, then revise the draft. Do not
accept a reviewer's new facts, constraints, or suggested fixes without support.
Keep the disposition of material findings in local review notes. Return material
changes and their affected evidence to the reviewer when those changes require
independent checking; purely mechanical edits need no new full review.

After the last prose edit, the author applies `humanizer` and then `stop-bullshit`
to the final document and any accompanying opening prompt. Retain required
uncertainty and source limits. Finalize only after the review and revision pass
are complete. If a reviewer fails or is unavailable, use another available agent;
if review cannot be completed, deliver only a clearly labeled draft with the
specific limitation. Do not silently substitute self-review.

Keep the document policy's publication and approval boundaries. Agent review
does not grant publication authority or require an extra user approval when the
final manuscript is already authorized. When concrete-manuscript approval is
required, present the reviewed revision for that approval before publication.
Report the saved location and any delivery limitation without inserting the review
transcript into the finished document.
