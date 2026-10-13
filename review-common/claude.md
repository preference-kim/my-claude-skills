# Claude review process

Before launch, read [authentication](../../agent-guidance/claude-auth.md) and
[model/fallback policy](../../agent-guidance/claude-model.md).
Resolve these links from this file's canonical directory.

Use a trusted directory and configuration: `--print` skips workspace trust.
Apply the caller's tool, permission, and mutation limits. Report blocked access
without approval or sandbox bypass flags.

```bash
env -u CLAUDE_CODE_OAUTH_TOKEN -u ANTHROPIC_API_KEY -u ANTHROPIC_AUTH_TOKEN \
  claude --print --model fable --fallback-model opus,sonnet --effort xhigh \
  --no-session-persistence --output-format json
```

Use top-level `result` as review text. Report the configured candidate from
`modelUsage`, excluding auxiliary models. Update aliases with canonical
`claude-model.md`.
