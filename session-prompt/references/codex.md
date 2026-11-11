# Prompts for OpenAI models in Codex

Read before rewriting a prompt for a Codex recipient. These checks summarize
OpenAI's guidance; when the pages are reachable and the recipient is a model
newer than GPT-6 Astra, read the current pages first, because guidance changes
by model:

- [Codex prompting](https://developers.openai.com/codex/prompting)
- [Codex best practices](https://developers.openai.com/codex/learn/best-practices)
- [Using the latest model](https://developers.openai.com/api/docs/guides/latest-model)

Shape the user's content as follows. A check that needs content the text lacks
becomes a supplement request, not an addition.

- **Four parts.** A reliable Codex prompt states the goal, the context (files,
  folders, documents, errors), the constraints, and what is true when the task
  is done. Order the user's content that way; request a missing part whose
  absence would make the recipient guess.
- **Point to the code.** Name file paths and reproduction steps explicitly;
  they matter more than a high-level description.
- **Say how to verify.** Keep the user's checks as the done condition. The model
  can stop early, so when the text decides it, say whether done includes running
  the code, checking the result, and fixing failures.
- **Approval after a reviewable result.** Keep the user's approval rules exact.
  Where the text asks for a review point, place it after a concrete result,
  not before work starts.
- **Priority among instructions.** The model follows `AGENTS.md` and skill
  instructions closely. When the text conflicts with instructions the recipient
  will load, request which takes priority.
- **Concrete behavior, plain paragraphs.** Describe the behavior wanted, not a
  tone label. Use short paragraphs and lists only for parallel or ordered items.
