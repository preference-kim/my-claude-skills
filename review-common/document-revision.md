# Document revision workflow

Handoffs and PR descriptions require a separate-agent review and revision before
final delivery. The owning document policy controls content and publication.

## Prepare the review

Read [humanizer](../humanizer/SKILL.md), [stop-bullshit](../stop-bullshit/SKILL.md),
and the applicable document policy before composing the brief. Give a separate
agent:

- The exact draft, purpose, audience, requested language, user requirements, and
  publication authority. Include a handoff's opening prompt.
- Relevant sources, claim-specific evidence, and explicit gaps. For PR descriptions,
  include the base/head diff and evidence for retained claims.
- The applicable AGENTS.md reasoning and communication principles, document policy,
  and conditional evidence contracts, plus both skills above. Supply readable
  canonical paths, or their contents when the reviewer cannot access those files.

Keep drafts and evidence within their authorized storage and audience.

## Reviewer contract

Inspect the draft and sources independently. Apply `humanizer` in embedded mode,
then `stop-bullshit` to the proposed prose, source claims, and your own feedback.
Preserve required structure, meaning, and warranted uncertainty. Prose editing
cannot supply missing evidence or justify a contradicted claim.

Check whether a reader without the conversation can follow material conclusions
and their support. Return supported findings with locations and proposed revisions,
plus unresolved source or scope gaps. Identify the reviewed version and anything
not checked. A no-finding result is valid.

The reviewer is a read-only leaf. It can propose text but cannot edit shared
artifacts, publish, contact others, invoke orchestration, or delegate.

## Revise and deliver

Evaluate findings against sources and requirements. Record material dispositions
in local review notes and apply supported revisions. Return material changes and
related evidence for independent checking when needed. Mechanical edits do not
require another full review.

After the last prose edit, the author applies `humanizer`, then `stop-bullshit`,
to the final document and any opening prompt. Complete the separate review and
revision before calling it final. If the reviewer fails, use another available
agent. If review remains unavailable, deliver a labeled draft with that limitation,
not an unreported substitution of self-review.

Agent review grants no publication authority. Use existing manuscript approval
when sufficient. Where the owning policy requires concrete-manuscript approval,
present the reviewed revision before publishing. Report the saved location and
any delivery limit without inserting the review transcript into the document.
