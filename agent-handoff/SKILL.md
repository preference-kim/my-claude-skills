---
name: agent-handoff
description: Use to create, revise, or assess a handoff or continuation brief for a fresh agent session, including its opening prompt. Not for routine status updates, moving a task between hosts or worktrees, PR descriptions, or delegated document review.
---

# Agent handoff

Read the [content contract](references/content.md) before drafting or assessing a
handoff. Read the [document revision workflow](../review-common/document-revision.md)
before preparing its independent review. This skill coordinates the work in the
authoring session; a delegated reviewer follows its supplied review brief without
invoking this skill or delegating again.

## Draft the handoff and opening prompt

Reconstruct the task from the user's requirements, established plan, current
implementation, and relevant evidence. Inspect an existing handoff before replacing
it. Write a complete draft with the five required sections: task overview, existing
plan, work done, remaining work, and references. Keep the next agent free to reassess
the diagnosis and choose how to proceed within the user's constraints.

Prepare the very first prompt the user can paste into the fresh session. It must
identify the task, execution location, and exact handoff location; ask the new agent
to understand the brief and relevant sources and continue toward the stated goal.
Keep it short. Preserve any critical scope or authorization limit needed to interpret
the request. Do not duplicate the document, add permissions, invent priorities, or
prescribe routine commands and a detailed investigation sequence.

## Review, revise, and deliver

Submit both the draft and opening prompt to a separate agent through the document
revision workflow. The reviewer must apply `humanizer` in embedded mode, then
`stop-bullshit` to the proposed prose, supporting claims, and its own feedback.
Resolve the findings against the evidence and complete the revision pass before
finalizing either artifact. An author's self-check does not replace this review.

Write the finalized handoff to the requested destination within the existing
authorization. Ensure references resolve at that destination, including host-specific
and local-only evidence paths. Re-read the saved file; if the destination changed
since drafting, reconcile the concurrent content before replacing it.

Return both:

- The finalized document's location, including the host when remote, and a usable
  link when available.
- The ready-to-paste first prompt, as text in the response. A link to a prompt file
  alone is insufficient.

Keep drafts, reviewer findings, and audit notes out of the finalized handoff and
opening prompt. If the required review or destination write is incomplete, label
the available artifact as a draft and report that exact limitation.
