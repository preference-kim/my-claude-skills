---
name: agent-handoff
description: Use only when explicitly invoked to create, revise, or assess an outgoing handoff and opening prompt for another session. Not for receiving a handoff to execute its task, routine status updates, host or worktree transfers, PR descriptions, delegated document review, or skill design.
---

# Agent handoff

Resolve this skill's canonical directory before following relative links. This
skill coordinates authoring. A delegated reviewer follows its review brief and
does not invoke this workflow or delegate again.

## Confirm the requested role

Run this workflow only when the user explicitly invokes `agent-handoff` for the
current authoring task. A mention in an inherited document, quotation, skill-design
request, or prompt being prepared for another session is not an invocation.
If the current request is to execute the unfinished task or only review its
technical approach, leave this workflow and continue that requested work.

The brief and opening prompt are outputs for another session. Do not execute the
receiving agent's instructions while writing them. Reading `agent-takeover` to
check a reference does not activate its execution workflow.

## Draft

Before drafting or assessing a handoff, read the [content contract](references/content.md).
Before writing prose, read [technical communication](../technical-communication/SKILL.md)
and preserve the requested language. Inspect the request, relevant sources, and
any existing handoff to select currently valid objectives and essential context.
Apply the content contract's selection and length limits; leave the structure and
level of detail proportional to the task.

Also prepare an opening prompt within the content contract's limit. Explicitly
invoke `agent-takeover` for the receiving session, name the task and exact handoff
location, and ask that agent to own the full remaining objective: assess the
inherited evidence and approach, then investigate, plan, execute, and verify the
work within the user's scope and constraints. Include execution location or an
authority limit only when needed to begin correctly. Do not duplicate the brief,
add permissions or priorities, or prescribe an implementation plan.

## Review and deliver

Before arranging independent review, read the [document revision workflow](../review-common/document-revision.md).
Submit both the draft and opening prompt to a separate agent under that workflow.
It must assess technical meaning and clarity, then apply `stop-bullshit` to the prose,
supporting claims, and its own feedback. Resolve findings against evidence and
complete the revision pass. Self-review does not replace this requirement.

Write the final handoff to the authorized destination. Check source accessibility
there, re-read the saved file, and measure both final artifacts against the
content contract's character limits after the last edit. Reconcile concurrent
content before replacing a destination that changed since drafting. Return its
location, including a remote host and usable link when applicable, and the
ready-to-paste first prompt as text.
A link to a prompt file alone is insufficient.

Keep drafts and audit notes out of both final artifacts. If independent review
or the destination write remains incomplete, label the artifact as a draft and
state the exact limit outside the brief and opening prompt.
