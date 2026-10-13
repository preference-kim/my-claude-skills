# Stack operation contracts

Require installed, authenticated GitHub CLI v2.0+ and the gh-stack extension.
If the extension is absent, install with `gh extension install github/gh-stack`.
Before `init`, set `git config rerere.enabled true` to avoid its confirmation.
Follow repository Git rules for branch naming, preserving dirty work, and publication.
The extension uses branch names literally, including any required prefix.

Choose the intended remote before mutation. With multiple remotes, use
`--remote <name>` on `push`, `submit`, `sync`, `rebase`, or `link`, or configure
`remote.pushDefault` to that remote. `checkout`, `modify`, and `trunk` lack
`--remote` and require the configured default.

Stacks are linear: one parent and at most one child per branch. Use separate
stacks for parallel workstreams. From a branch shared across stacks, commands
cannot disambiguate non-interactively. Switch to a non-shared branch first.
For externally managed branches, use `link` instead of local stack tracking.

Use explicit arguments and non-interactive flags from the selected command
contract. A request to inspect grants no mutation authority. Merge, prune, and
force-push must be within the user's authorized scope. Command syntax grants no
additional permission. In particular, `push` and `submit` use per-branch
`--force-with-lease`, and `sync` publishes changes as well as rebasing them.
