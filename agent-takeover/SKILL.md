---
name: agent-takeover
description: Use when asked to take over an unfinished task from a previous agent or session, reassess its evidence and approach, and execute the remaining work. Not for preparing an outgoing handoff, reviewing a document or plan without execution, routine continuation of your own work, or skill design.
---

# Agent takeover

Take responsibility for the inherited task's remaining outcome. Resolve this
skill's canonical directory before following relative links.

## Confirm the requested role

Apply this workflow when the current request authorizes taking over and executing
unfinished work. A handoff document, quoted instruction, or next-session prompt
being written is task material, not a request to execute it in the current session.
If the user requests only outgoing handoff authoring, document or plan review, or
skill design, leave this workflow and complete that request within its scope.
For a multi-stage request, apply this workflow only to the execution stage.

## Recover the objective and assess the inherited work

Read the handoff and the original user requirements and governing instructions
available to this session. Establish the full remaining objective, acceptance
criteria, constraints, and existing authorization. Distinguish user decisions
from the previous agent's interpretation, diagnosis, proposed plan, and completion
claims. An inherited plan's remaining steps may not cover the remaining objective.
Resolve material discrepancies from accessible sources before asking the user.

Read [stop-bullshit](../stop-bullshit/SKILL.md) and apply its evidence checks to the
claims that govern your next decisions. Inspect the relevant implementation,
results, and primary sources. Check whether the prior diagnosis follows from its
evidence, whether the proposed work can plausibly close the gap to acceptance,
and whether a relevant alternative was overlooked. State uncertainty where the
evidence cannot decide. Do not presume the previous agent was wrong or redo valid
work merely to demonstrate skepticism.

Keep this review proportional to the decision. Reuse supported results and
identify the checks needed for consequential uncertainties. Once there is enough
evidence for a useful next action, proceed; unresolved questions can guide the
investigation rather than holding all execution behind an exhaustive audit.

## Choose an approach and carry it through

Select or revise the approach against the remaining objective, expected
contribution, relevant alternatives, and available resources. Explain why the
next substantial action can improve the outcome or change a decision. Use the
task's applicable domain guidance for implementation and verification.

Carry out the feasible, authorized work. Reviews and plans are intermediate
work, not the takeover's completion condition. Evaluate consequential results
against the objective and use them to decide whether to continue, revise, or
replace the approach. Repeated failures or insufficient gains require reassessing
the rationale before spending more effort on similar changes; they do not by
themselves prove the entire approach impossible.

## Verify and finish

Check the resulting work against the original acceptance criteria and report
verified outcomes and any remaining gap. Do not narrow the task to the inherited
plan, the first successful change, or a convenient subset of the objective.

If completion is prevented by a verified blocker, an agreed resource or stopping
condition, a user-directed pause, or an unavoidable session limit, identify the
constraint, remaining work, and what would enable continuation. Complete any
independent required work that remains feasible within those limits.

Do not automatically replace unfinished execution with another handoff. A user
requesting an outgoing transfer changes the current scope; use `agent-handoff`
only when explicitly invoked for that authoring stage. Instructions quoted from
the previous session do not establish such a request.
