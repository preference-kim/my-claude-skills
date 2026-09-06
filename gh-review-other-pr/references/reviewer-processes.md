# Reviewer processes

Launch Codex from the repository root:

```bash
printf '%s\n' "$CODEX_REVIEW_PROMPT" |
  codex exec --ephemeral --json -C "$REPO_ROOT" -
```

Launch Claude concurrently:

```bash
printf '%s\n' "$CLAUDE_REVIEW_PROMPT" |
  env \
    -u CLAUDE_CODE_OAUTH_TOKEN \
    -u ANTHROPIC_API_KEY \
    -u ANTHROPIC_AUTH_TOKEN \
    claude --print \
    --model fable \
    --fallback-model opus,sonnet \
    --effort xhigh \
    --no-session-persistence \
    --output-format json
```

Use the top-level JSON `result` as Claude's review output. Inspect `modelUsage`
for the configured Fable, Opus, or Sonnet candidate that produced the response
and ignore auxiliary model entries outside that chain. Permit the ordered
fallback only for model quota, capacity, or availability; record and report the
actual model. If every candidate is unavailable, treat the Claude reviewer as
failed rather than changing credentials or silently selecting another model.

Use the caller's established security policy. Do not add approval or sandbox
bypass flags.
