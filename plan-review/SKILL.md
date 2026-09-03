---
name: plan-review
description: Independently review, critique, validate, or stress-test an existing implementation or subtask plan. Do not use merely because a request creates or discusses a plan.
---

# Plan Review

Obtain a rigorous review of an existing plan from the opposite agent family. The review is read-only unless the user separately authorizes an update to a specific plan artifact.

## Resolve the review target

- Review only a plan file explicitly identified by the user or plan content that is uniquely identifiable in the conversation.
- Resolve an explicit file path as supplied, expanding `~` when needed. A tool-specific path is valid when the user identifies it directly.
- Never scan a tool-specific plan directory, select a newest or recent file, join a vague label to a default directory, or otherwise guess among candidates.
- If the request does not identify exactly one plan, ask the user to identify the target and stop.

## Preserve the authorization boundary

- Treat review as read-only. Neither the reviewer nor the calling agent may modify the plan, workspace, version control, or external state merely because a review was requested.
- Produce a complete replacement plan only when the user requests one.
- Update a plan file only when the user explicitly asks to update that identified file. Apply any authorized update in the calling agent after the independent review; never grant the reviewer write access.
- Do not control plan-mode transitions, approval UI, or tool-specific workflow state. Return the review and wait for the user's next instruction.

## Select an independent reviewer

Read [references/reviewer-adapters.md](references/reviewer-adapters.md), then use the available opposite-family reviewer with the configured highest model as the primary and `xhigh` effort:

- From Codex, use Claude.
- From Claude, use Codex.

Use a lower model only through the adapter's ordered fallback chain and only when the primary is unavailable because of model quota, capacity, or availability. A fallback result is still independent, but report the actual model and do not describe it as a highest-model review. Do not substitute the same agent family, the calling agent's self-review, an unconfigured lower model, or lower effort. If the current agent family cannot be determined or every configured reviewer model is unavailable, report that independent review is blocked and state the failed prerequisite.

## Run the review

Read [references/review-criteria.md](references/review-criteria.md) and [references/reviewer-prompt.md](references/reviewer-prompt.md). Give the reviewer:

- the exact plan content or resolved plan path;
- the user's review request, including whether a replacement plan was requested;
- only the source files, repository instructions, and raw evidence needed to verify the plan.

Do not provide the calling agent's expected verdict, suspected defects, preferred redesign, or draft findings. Require the reviewer to remain read-only and not to delegate further.

## Return the result

Report the independent review without silently changing the plan:

- reviewer family and actual model, including whether a configured fallback was used;
- verdict: `Approve`, `Revise`, or `Reject`;
- concise rationale and evidence-backed material findings;
- required changes, if any;
- reproducible verification or acceptance conditions.

Include a proposed replacement plan only when the user requested one. If the user explicitly authorized updating a named plan file, apply the reviewed changes after presenting or recording the review, re-read the file, and report what was updated.
