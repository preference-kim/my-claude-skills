---
name: agent-handoff
description: Use to create, revise, or assess a handoff or continuation brief for a fresh agent session, including its opening prompt. Not for routine status updates, moving a task between hosts or worktrees, PR descriptions, or delegated document review.
---

# Agent handoff

Resolve this skill's canonical directory before following relative links. This
skill coordinates authoring. A delegated reviewer follows its review brief and
does not invoke this workflow or delegate again.

## Draft

Before drafting or assessing a handoff, read the [content contract](references/content.md).
Before writing prose, read [technical communication](../technical-communication/SKILL.md)
and preserve the requested language. Reconstruct the task from the request,
accepted plan, implementation, and evidence. Inspect an existing handoff before
replacing it. Draft its five required sections without prescribing a new plan
for the receiving agent.

Also prepare a short first prompt the user can paste into a fresh session. Name
the task, execution location, and exact handoff location. Ask the next agent to
read the brief and relevant sources, then continue toward the goal. Preserve
critical scope and authority limits. Do not duplicate the brief, add permissions
or priorities, or prescribe routine commands.

## Review and deliver

Before arranging independent review, read the [document revision workflow](../review-common/document-revision.md).
Submit both the draft and opening prompt to a separate agent under that workflow.
It must assess technical meaning and clarity, then apply `stop-bullshit` to the prose,
supporting claims, and its own feedback. Resolve findings against evidence and
complete the revision pass. Self-review does not replace this requirement.

Write the final handoff to the authorized destination. Check source accessibility
there and re-read the saved file. Reconcile concurrent content before replacing a
destination that changed since drafting. Return its location, including a remote
host and usable link when applicable, and the ready-to-paste first prompt as text.
A link to a prompt file alone is insufficient.

Keep drafts and audit notes out of both final artifacts. If independent review
or the destination write remains incomplete, label the artifact as a draft and
state the exact limit.
