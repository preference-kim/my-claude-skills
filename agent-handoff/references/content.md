# Handoff content contract

A handoff gives a fresh session a clean starting point when accumulated context
has become cluttered. Preserve only currently valid objectives and the
references and context essential to pursuing them. The receiving agent owns
its investigation, implementation choices, and next plan.

## Select what remains relevant

State what still needs to be accomplished, the scope and acceptance criteria,
and binding user requirements or decisions. Remove completed or superseded goals
unless their result is essential context for an active objective. Do not carry
forward the previous agent's proposed plan, diagnosis, or implementation
preferences as instructions. State current scope directly instead of reciting
superseded goals or unapproved proposals.

Retain a fact only when omitting it would materially hinder continuation or cause
a known constraint to be missed. Relevant context can include the work location,
uncommitted changes, active jobs or locks, authority limits, unresolved blockers,
and a short account of consequential results. Include these only when they apply;
there are no mandatory status fields or section template. Keep material facts
and their limits in the body, distinguish observations from hypotheses, and do
not turn partial validation into completion. Preserve recorded status; missing
information does not establish absence or invalidate a supplied result. Keep
handoff-authoring and review notes outside the brief and opening prompt.

Preserve essential sources with precise, accessible links or paths and a short
explanation of their relevance. Examples include confirmed server availability
notices, Jira tickets, relevant Slack threads, and evidence needed to understand
current work. For mutable facts, retain the recorded time or validity window;
identify consequential uncertainty rather than inventing freshness. Identify
hosts and path roots when needed to access a source. For another environment,
carry the essential facts and accessible references; identify evidence that
will not travel with Git.

Do not reproduce an implementation tour, session chronology, speculative fixes,
routine commands, or detailed next steps. Link maintained sources instead of
copying them. Retain a failed approach or prior decision only when it establishes
an essential constraint, with its evidence and limits; leave reassessment to the
receiving agent. Do not start implementation or experiments to fill a handoff.

## Length limits

- Handoff document: at most **7,000 characters**.
- Opening prompt: at most **500 characters**.

Count Unicode characters in the complete source text, including spaces,
newlines, Markdown, and URLs. These are ceilings, not targets. Measure the saved
document and the exact ready-to-paste prompt after the last edit. Remove
nonessential material rather than compressing it into cryptic prose or moving
overflow into extra handoff files, appendices, or the opening prompt. Existing
source references remain useful; a linked continuation of the handoff does not
bypass the limit.

## Acceptance check

A reader without the conversation can identify the valid objectives, binding
constraints, and essential sources/context, then investigate and decide how to
continue independently. Every retained detail serves that purpose. Resolve
contradictions and unsupported claims; preserve consequential uncertainty and
authority boundaries. Both artifacts fit their limits and carry no stale agenda
or unnecessary instructions from the previous session.
