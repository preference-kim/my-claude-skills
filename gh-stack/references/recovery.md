## Output conventions

- **Status messages** go to **stderr** with emoji prefixes: `✓` (success), `✗` (error), `⚠` (warning), `ℹ` (info).
- **Data output** (e.g., `view --json`) goes to **stdout**.
- When piping output, use `2>/dev/null` to suppress status messages if only data output is needed.

## Exit codes and error recovery

| Code | Meaning | Agent action |
|------|---------|-------------|
| 0 | Success or sync cancellation | Check for `ℹ Sync aborted` and verify stack state before reporting synchronization complete |
| 1 | Generic error | Read stderr for details; may indicate commit/push failure |
| 2 | Not in a stack | Run `gh stack init` to create a stack first |
| 3 | Rebase conflict | Parse stderr for conflicted file paths, resolve conflicts, run `gh stack rebase --continue` |
| 4 | GitHub API failure | Check `gh auth status`, retry the command |
| 5 | Invalid arguments | Fix the command invocation (check flags and arguments) |
| 6 | Disambiguation required | A branch belongs to multiple stacks. Run `gh stack checkout <specific-branch>` to switch to a non-shared branch first |
| 7 | Rebase already in progress | Run `gh stack rebase --continue` (after resolving conflicts) or `gh stack rebase --abort` to start over |
| 8 | Stack is locked | Another `gh stack` process is writing the stack file. Wait and retry — the lock times out after 5 seconds |
| 9 | Stacked PRs unavailable | The repository does not have stacked PRs enabled. Tell the user that stacks must be enabled on the repository first |
| 10 | Modify recovery required | A `gh stack modify` session was interrupted. This skill does not use `modify`, so agents should not produce this; if the repo is left in this state, run `gh stack modify --abort` to restore the pre-modify state |

## Known limitations

1. **Stacks are strictly linear.** Branching stacks (multiple children on a single parent) are not supported. Each branch has exactly one parent and at most one child. If you need parallel workstreams, use separate stacks.
2. **Stack disambiguation cannot be bypassed.** If the current branch is the trunk of multiple stacks, commands error with code 6. Check out a non-shared branch first.
3. **Multiple remotes require `--remote` or config.** If more than one remote is configured, set `remote.pushDefault` in git config, or pass `--remote <name>` to the commands that accept it (`push`, `submit`, `sync`, `rebase`, `link`). `checkout`, `modify`, and `trunk` have no `--remote` flag and rely on `remote.pushDefault`.
4. **Remote stack checkout requires a stack or PR number.** `checkout` with a branch name only works with locally tracked stacks. Use a stack number or PR number (e.g. `gh stack checkout 7` or `gh stack checkout 123`) to pull a stack from GitHub.
5. **PR title and body are auto-generated.** There is no flag to set a custom PR title or body during `submit`. The title and body are generated from commit messages plus a footer. Use `gh pr edit` to modify PR title and body after creation.

## Handle rebase conflicts (agent workflow)

When `sync` exits with code 3, its attempted rebases have already been rolled
back. Start `gh stack rebase` to enter the resumable recovery workflow. Read the
conflicting files reported on stderr, resolve them, and stage the resolved paths
with `git add`. Run `gh stack rebase --continue`; repeat resolution and staging
for each subsequent conflict. If recovery cannot proceed, use
`gh stack rebase --abort` to restore the original state.
