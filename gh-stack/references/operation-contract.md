# Stack operation contracts

Require installed, authenticated GitHub CLI v2.0+ and the gh-stack extension.
If the extension is absent, install with `gh extension install github/gh-stack`.
Before `init`, set `git config rerere.enabled true` to avoid its confirmation.
Follow repository Git rules for branch naming, preserving dirty work, and publication.
The extension uses branch names literally, including any required prefix.

Before mutation, verify both the intended Git remote and the GitHub API target
repository. Do not assume `--remote` or `remote.pushDefault` also selects the API
repository. With multiple remotes, use
`--remote <name>` on `push`, `submit`, `sync`, `rebase`, or `link`, or configure
`remote.pushDefault` to that remote. `checkout`, `modify`, and `trunk` lack
`--remote` and require the configured default.

Rely on `gh repo set-default` only after verifying that the installed extension
honors it. If it does not, upgrade to a verified fixed release or set
`GH_REPO=HOST/OWNER/REPO` for the individual command. Confirm the API target
matches the intended repository before proceeding.

Stacks are linear: one parent and at most one child per branch. Use separate
stacks for parallel workstreams. From a branch shared across stacks, commands
cannot disambiguate non-interactively. Switch to a non-shared branch first.
For externally managed branches, use `link` instead of local stack tracking.

Use explicit arguments and non-interactive flags from the selected command
contract. A request to inspect grants no mutation authority. Merge, prune, and
force-push must be within the user's authorized scope. Command syntax grants no
additional permission. In particular, `push` and `submit` use per-branch
`--force-with-lease`, and `sync` publishes changes as well as rebasing them.
