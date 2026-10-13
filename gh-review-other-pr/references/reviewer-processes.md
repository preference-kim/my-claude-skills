# Reviewer processes

Launch Codex from the repository root:

```bash
printf '%s\n' "$CODEX_REVIEW_PROMPT" |
  codex exec --ephemeral --json -C "$REPO_ROOT" -
```

Before checking Claude authentication or launching, read the [shared Claude adapter](../../review-common/claude.md)
for its command, authentication, model and fallback, trusted configuration, and
result handling. Launch it concurrently with Codex and pass
`$CLAUDE_REVIEW_PROMPT` on stdin.

Both reviewers use this workflow's read-only permissions and the caller's security
policy. Do not add approval or sandbox bypass flags.
