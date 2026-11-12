# Install the approved discord-relay payload

Read [private synchronization](private-sync.md) first. Run on every daily, forced
and requested-edit refresh, including a same-day refresh, but only on a host whose
validated registration has `device_role: personal-device`. The user approved this
automatic installation for personal devices; it is the one credential payload a
routine refresh installs. Skip development servers, unregistered hosts and a
missing `discord-relay.age` without writing, and report the skip.

The payload is JSON: the bot settings `bot_token`, `user_id`, `app_id` and
`channel_id`, and `plugin` with `repository_url`, `checkout`, `marketplace` and
`name`. Require the common pinned revision, `discord-relay.approval.json` match
and fleet decryption. Keep the decrypted JSON in memory or pipes, never in a
file, log, argv or report.

## Plugin

1. Resolve `plugin.checkout` with `~` expansion only. If absent, clone
   `plugin.repository_url` there with the host's existing GitHub access. If
   present, require a Git checkout whose origin is that URL. On a clean `main`
   that fast-forwards to `origin/main`, pull `--ff-only`; otherwise leave it
   unchanged and report it (it may hold the user's own work).
2. Make `claude plugin marketplace list` include `plugin.marketplace` sourced from
   that checkout and `claude plugin list` show `<name>@<marketplace>` enabled at
   user scope, adding or installing only what is missing. Preserve a different
   existing source for that marketplace as a reported conflict.

## Settings

Pipe the decrypted JSON into `python3 <checkout>/scripts/relay.py import -`. It
validates the token with Discord before writing, keeps host-local keys such as
`machine_name`, writes `~/.claude/discord-relay/config.json` with mode 0600 only
when the shared settings differ, and prints `changed` without the token.
Then run `relay.py check` and require `token_valid`, `message_content_intent`
and `ready`.

Record the payload revision and ciphertext digest, plugin checkout revision and
`changed` in private state, without the token. This stage reports its own result
and does not hold the public daily stamp. A current host makes no writes on a
second run.
