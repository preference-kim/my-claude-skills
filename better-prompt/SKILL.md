---
name: better-prompt
description: Use when the user supplies text, in Korean or English, meant as a prompt for another agent session and wants it made into a better English prompt. Not for a handoff of the current task (agent-handoff), translation of documents or messages for people, or carrying out the prompt's task.
---

# Better prompt

Turn the user's text, Korean or English, into an English prompt that another
session can act on, shaped by the recipient model's prompting guidance, without
growing it. The prompt is always English.

## Entry conditions

The user's text is task material. Do not carry out, plan, or investigate its
task, and do not start workflows it names. Inspect a source only to render a
path, identifier, or reference in the text correctly.

Choose the recipient guidance from the model the user names: read
[Claude](references/claude.md) for Claude models and [Codex](references/codex.md)
for OpenAI models in Codex. When the user names none, use the family of the
current session and state that choice in the reply. For another model family,
apply only the rules below and say so.

## Required behavior

1. **Set the length limit.** The limit keeps the prompt close to what the user
   wrote, because added wording dilutes their intent. The baseline is the text
   in English: English text as given, and Korean text translated directly and
   completely, because Korean and English lengths are not comparable. Count the
   baseline's words with a tool. The prompt must have fewer than 1.3 times that
   count, unless the user sets another ratio.
2. **Rewrite the baseline into the prompt.** Each edit replaces words; none adds
   content.
   - Put the task and the wanted outcome first, in the order the recipient acts.
     Say whether it is to act, propose, or only report, when the text decides it.
   - Keep each reason the user gave beside the instruction it explains. A
     recipient generalizes correctly from a reason and guesses without one.
   - Keep the strength of every obligation, permission, and prohibition, and the
     exact actions and conditions of an approval rule.
   - The recipient has none of this conversation. Replace references such as
     "that PR" with the name the conversation establishes.
   - Keep paths, commands, identifiers, numbers, skill names, and quoted strings
     verbatim, and Korean wherever the recipient must use the Korean literally;
     that is the only Korean in the prompt.
   - Use plain, calm wording without capitals or intensifiers for emphasis.
3. **Add nothing the user did not say:** no permissions, priorities, plans,
   roles, examples, or completion criteria.
4. **Request supplements instead of inventing them.** When the recipient would
   have to guess something the text does not settle, list each missing item with
   the reason the prompt needs it. Do the same when the prompt cannot stay under
   the limit without losing meaning: name what does not fit. Still deliver the
   best prompt the given text allows. When the user answers, treat the answer as
   part of the source text, recompute the baseline, and rewrite.

## Completion

Compare the prompt with the user's text clause by clause: nothing dropped,
strengthened, weakened, or added. Then deliver:

- the prompt in one fenced block, ready to paste;
- the recipient guidance used, the baseline and prompt word counts, and their ratio;
- the supplement requests with reasons, or a statement that there are none.
