# Opposite-Agent Reviewer Adapters

This file contains runtime-specific configuration. The review contract, criteria, and output remain tool-neutral.

## Current reviewer selection

| Calling agent | Independent reviewer | Model | Effort |
| --- | --- | --- | --- |
| Codex | Claude Code | `fable` | `xhigh` |
| Claude Code | Codex | `sol` | `xhigh` |

These aliases represent the current highest configured models for each family. Update this table and the matching invocation when the configured highest model changes; do not embed model aliases in the shared review criteria or prompt.

Prefer a native opposite-agent delegation facility when it can enforce the same model, effort, isolation, and read-only boundary. Otherwise use the corresponding non-interactive CLI adapter below.

## Codex calling Claude

Require `claude` and a valid subscription login managed by `claude auth login` or `/login`. Do not load a token from `$HOME/.claude/oauth-token`. Remove inherited credential overrides from the Claude child process so they cannot take precedence over the CLI-managed login, then invoke the equivalent of:

```bash
env \
  -u CLAUDE_CODE_OAUTH_TOKEN \
  -u ANTHROPIC_API_KEY \
  -u ANTHROPIC_AUTH_TOKEN \
  claude --print \
  --model fable \
  --effort xhigh \
  --permission-mode dontAsk \
  --no-session-persistence \
  --disable-slash-commands \
  --tools "Read,Glob,Grep" \
  --output-format text
```

Pass the composed reviewer prompt on standard input or as the non-interactive prompt. The restricted tool list keeps the reviewer read-only and disables shell, browser, messaging, and external mutation tools. A successful reviewer request is the authentication check; `claude auth status` alone does not prove that a configured credential is accepted by the service.

If the managed login is unavailable or cannot refresh, report the authentication prerequisite as a blocker and ask the user to run `claude auth login`. Do not start the login flow or create and persist a fallback token without explicit authorization.

In CI or another browserless environment where the managed login is unavailable, inject a token produced by `claude setup-token` as `CLAUDE_CODE_OAUTH_TOKEN` through the environment's secret manager. Do not persist the token in the repository or a shared plaintext token file.

## Claude calling Codex

Require `codex` and valid Codex authentication. Invoke a fresh non-interactive reviewer with the equivalent of:

```bash
codex exec --ephemeral \
  --model sol \
  --config 'model_reasoning_effort="xhigh"' \
  --sandbox read-only \
  --ask-for-approval never \
  --cd "<relevant-project-root>" \
  -
```

Pass the composed reviewer prompt on standard input. Keep the sandbox read-only and approvals disabled. Instruct the reviewer not to invoke skills, subagents, or nested review workflows.

## Unavailable reviewer

If the opposite CLI or delegation facility, required model, authentication, or read-only execution boundary is unavailable, stop and report that independent review is blocked. Include the failed prerequisite; do not fall back to the calling family or silently change model or effort.
