## Prerequisites

The GitHub CLI (`gh`) v2.0+ must be installed and authenticated. Install the extension with:

```bash
gh extension install github/gh-stack
```

Before using `gh stack`, configure git to prevent interactive prompts:

```bash
git config rerere.enabled true           # remember conflict resolutions (skips prompt on init)
git config remote.pushDefault origin     # if multiple remotes exist (skips remote picker)
```

## Agent rules

**All `gh stack` commands must be run non-interactively.** Every command invocation must include the flags and positional arguments needed to avoid prompts, TUIs, and interactive menus. If a command would prompt for input, it will hang indefinitely.

1. **Always supply branch names as positional arguments** to `init`, `add`, and `checkout`. Running these commands without arguments triggers interactive prompts. Branch names are used exactly as given — a name is never prefixed or transformed, so `gh stack add refactor/foo` creates a branch named `refactor/foo`.
2. **Always use `--auto` with `gh stack submit`** to auto-generate PR titles. Without `--auto`, `submit` prompts for a title for each new PR.
3. **Always use `--json` with `gh stack view`.** Without `--json`, the command launches an interactive TUI that cannot be operated by agents. There is no other appropriate flag — always pass `--json`.
4. **Handle multiple remotes.** If more than one remote is configured, pre-configure `git config remote.pushDefault origin`, or pass `--remote <name>` to the commands that accept it: `push`, `submit`, `sync`, `rebase`, and `link`. `checkout`, `modify`, and `trunk` resolve a remote but have **no `--remote` flag** — they rely on `remote.pushDefault`. With multiple remotes and no configured default, these commands exit with an error in non-interactive mode.
5. **Avoid branches shared across multiple stacks.** If a branch belongs to multiple stacks, commands exit with code 6. Check out a non-shared branch first.
6. **Plan your stack layers by dependency order before writing code.** Foundational changes (models, APIs, shared utilities) go in lower branches; dependent changes (UI, consumers) go in higher branches. Think through the dependency chain before running `gh stack init`.
7. **Use standard `git add` and `git commit` for staging and committing.** This gives you full control over which changes go into each branch. The `-Am` shortcut is available but should not be the default approach—stacked PRs are most effective when each branch contains a deliberate, logical set of changes.
8. **Navigate down the stack when you need to change a lower layer.** If you're working on a frontend branch and realize you need API changes, don't hack around it at the current layer. Navigate to the appropriate branch (`gh stack down`, `gh stack checkout`, or `gh stack bottom`), make and commit the changes there, run `gh stack rebase --upstack`, then navigate back up to continue.
9. **Use `gh stack link` for external tool workflows.** When branches are managed by an external tool (jj, Sapling, etc.), use `gh stack link branch-a branch-b`. `link` does not rely on local tracking state and is intended for API-driven PR and stack management. Provide at least two branches/PRs to create or update a stack, or a stack number followed by the new branches/PRs to append them to the top of an existing stack (e.g. `gh stack link 7 branch-c`).
10. **Use `gh stack merge --yes` to merge stacked PRs.** `gh pr merge` does not work with stacked PRs. In a non-interactive terminal `gh stack merge` runs without prompting and merges the entire stack (bottom to top) atomically; pass `--yes` to be explicit. Scope the merge by passing a pull request number (`gh stack merge 42 --yes` merges everything up to and including PR #42) or a stack number (`gh stack merge 7 --yes`, which needs no local checkout). Choose the method with `--squash`, `--rebase`, `--merge`, or `--merge-method <method>`; without one, the last-used method is used. The merge is all-or-nothing — if any PR can't be merged, none are, and the failure reason is reported. Only basic pull request state is checked before merging (open and not a draft); bypassing merge requirements is not supported for stacks. If the base branch uses a merge queue, the stack is added to the queue instead of merging directly: the queue chooses the merge method (any method you pass is ignored with a warning), and the pull requests are added to the queue together but merge as the queue processes them, so they may land in separate groups rather than all at once.

**Never do any of the following — each triggers an interactive prompt or TUI that will hang:**
- ❌ `gh stack view` or `gh stack view --short` — always use `gh stack view --json`
- ❌ `gh stack submit` without `--auto` — always use `gh stack submit --auto`
- ❌ `gh stack init` without branch arguments — always provide branch names
- ❌ `gh stack add` without a branch name — always provide a branch name
- ❌ `gh stack checkout` without an argument — always provide a PR number or branch name
- ❌ `gh stack checkout <pr-number>` when a different local stack already exists on those branches — this triggers an unbypassable conflict resolution prompt; use `gh stack unstack --local` first to remove the local tracking state (this keeps the stack on GitHub intact), then retry the checkout
