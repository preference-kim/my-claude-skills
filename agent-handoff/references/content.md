# Handoff content contract

The handoff must support continuation without the conversation. Explain the
current task state in the body. References support verification, and the next
agent remains free to reassess the diagnosis and approach. Use these five sections
in order.

## 1. Task overview

State the goal, requirements, scope, and acceptance criteria before PR numbers
or shorthand. Identify the repository, checkout, branch, relevant revision, and
execution host or cluster. Distinguish the writer's host from execution hosts.
Include uncommitted work, active jobs, and task-specific authority or restrictions
when they affect continuation. Give the recorded observation time for mutable
state. Leave unavailable times unknown and identify consequential unchecked state.

## 2. Existing plan

Explain the established parts, their purpose, intended results, responsibilities,
dependencies, and rationale. Distinguish user requirements, accepted decisions,
and the previous agent's proposals. Label a reconstructed plan. If no plan is
recoverable, say so. Put progress below and new suggestions under remaining work.

## 3. Work done

Map the plan to completed, partial, or unverified results. Preserve the recorded
status: "unfinished" alone does not establish "not started" or "absent." For each
material result, explain the change and point to implementation symbols or files,
tests, and evidence. State validation conditions and scope. Distinguish implemented,
tested, committed, published, and accepted. A historical run or sample supports
only its recorded conditions.

## 4. Remaining work

For each material unresolved problem, connect triggering conditions, observed and
required behavior, impact, and evidence. Separate established causes from
hypotheses. Include failed approaches only when they change the next decision.
State the outcomes and dependencies still required, including unfinished
integration, validation, or delivery when the task requires them.

Define what establishes resolution. Tie a proposed fix to evidence or label it
as a hypothesis. Preserve binding constraints. Mark optional investigation ideas
as suggestions with their rationale. Leave routine commands, diagnostic choices,
and the next execution plan to the receiving agent.

## 5. References

Map sources selectively to the requirements, design, implementation, reproducer,
results, and discussions they establish. Cite precise inspected passages, symbols,
or results beside material claims. Define path roots and hosts. Same-environment
handoffs can use accessible local files but must identify what does not travel
with Git. For another environment, include the necessary facts and accessible
sources or reproducible instructions. Keep decision-critical methods and results
in the body. A directory or hash alone does not explain or verify a claim.

## Acceptance check

A reader must be able to explain the goal, established plan, current work and
locations, remaining obligations, and their evidence. Resolve contradictions and
unsupported completion claims. State consequential gaps once without inventing
dates, dependencies, status, or authority. Do not start new implementation or
experiments merely to fill a handoff.

Organize around current state, not session history. Remove repeated conclusions,
superseded instructions, conversational corrections, and incidental command logs.
Reference maintained procedures instead of copying them. Retain task-specific
exceptions, unavailable prerequisites, and any detail needed to understand or
verify a material claim.
