# Update active installed CLIs

After repository preflight, under the agent-update lock, check `claude`,
`codex` and `gh` on every full daily, forced or requested-edit refresh. Only
same-day daily refreshes may skip this work; SSH remains independent.

1. Record `command -v`, all PATH-visible installations, resolved targets and
   before versions. Identify the selected executable's owning installation
   channel. An absent command is reported, not installed.
2. Update only that active installation through its owner:
   - Native Claude: `claude update` on `latest`; switch a native `stable`
     channel with `claude install latest`. Package-managed Claude uses that
     manager's documented latest-channel command.
   - Codex: `codex update` if supported, otherwise the existing package or
     standalone installer's documented update. App-bundled binaries belong to
     the desktop app; update a separately installed CLI or report app ownership,
     never replace its bundle in place.
   - GitHub: compare `gh --version` with
     `gh api repos/cli/cli/releases/latest --jq .tag_name` (use the public API
     directly if needed), then update the owning manager's `gh` package.
3. Scope updates to the named package and necessary dependencies, retaining the
   installation method, configured repositories/taps and trust/signature
   checks. Use existing noninteractive authorization only; package-wide upgrades,
   new package managers, password prompts or privilege-policy changes are outside
   scope.
4. Re-resolve the active command and compare its after version with the native
   updater, registry or official release source. A shadowed update does not
   update the active command. Verify an updated Codex through external
   `codex --version`; an already-running process keeps its old in-memory version
   until restart, which must be reported.

Continue other CLI checks and safe repository/link work after a failure.
A known-outdated CLI that remains unupdated, shadowed or unverified blocks
`last-successful-sync`. Report installed/target versions when known, failure,
missing privilege and required recovery. An unavailable latest-version lookup
is a verification limit, not evidence that the installation is current.
