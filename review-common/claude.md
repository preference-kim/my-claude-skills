# Claude review process

Before launching, read the canonical dotfiles `agent-guidance/claude-auth.md` and
`agent-guidance/claude-model.md` (resolve from this directory's parent skills repo).
Use a fresh process with subscription-managed authentication, configured model
and ordered resource-only fallback, `xhigh` effort, no session persistence, and
JSON output. Remove inherited credential overrides only from the child.

The invoking workflow determines tools and mutation authority; never inherit the
other-PR or own-PR permission boundary from a different workflow. Use `result` as
review text and `modelUsage` to disclose the actual configured candidate used.

```bash
env -u CLAUDE_CODE_OAUTH_TOKEN -u ANTHROPIC_API_KEY -u ANTHROPIC_AUTH_TOKEN \
  claude --print --model fable --fallback-model opus,sonnet --effort xhigh \
  --no-session-persistence --output-format json
```

Apply the caller's tool restrictions to this command. No sandbox or approval bypass
is implied. Update the model alias together with canonical claude-model.md when the
configured primary changes.
