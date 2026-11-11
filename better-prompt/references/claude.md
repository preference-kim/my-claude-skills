# Prompts for Claude models

Read before rewriting a prompt for a Claude recipient. These checks summarize
Anthropic's guidance; when the pages are reachable and the recipient is a model
newer than they describe here, read its page first, because guidance changes by
model:

- [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [Prompting Claude Fable 5.2](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2)

Shape the user's content as follows. A check that needs content the text lacks
becomes a supplement request, not an addition.

- **Be direct about action.** Claude does what the wording asks: "suggest" yields
  suggestions and "change" yields edits. Use the verb that matches the user's intent.
- **Give the reason.** Claude generalizes from an instruction's reason. Request
  the reason for a constraint whose purpose the recipient must infer.
- **Say what to do.** Phrase an instruction as the wanted behavior where the text
  allows; keep the user's prohibitions.
- **Calm emphasis.** Current models overapply instructions marked as critical.
  State each rule once in normal wording.
- **Approval rules are applied as written.** Name the exact actions that need
  approval and those that need none, and keep the go-ahead condition inside the
  rule. Request the missing side when the text names only one.
- **Code ownership changes behavior.** When the text says the recipient owns the
  code and should improve it, say so plainly; when the text wants code changed as
  little as possible, do not imply ownership.
- **Structure only mixed content.** Put long pasted material first and the
  request after it, and wrap distinct materials in XML tags. Write plain
  instructions as prose.
