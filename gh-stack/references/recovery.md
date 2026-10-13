# Output and recovery

Status messages use stderr; `view --json` data uses stdout. Preserve diagnostics
until the operation's result is understood. Before retrying a failed mutation,
inspect actual branch and PR state, including partial publication.

| Code | Meaning | Required response |
| --- | --- | --- |
| 0 | Success or sync cancellation | Check `Sync aborted` and resulting state before claiming completion |
| 1 | Generic failure | Inspect stderr and possible commit/push effects |
| 2 | Not in a stack or unknown stack | Verify the target; initialize only if a new stack is intended |
| 3 | Rebase conflict | Follow the recovery procedure below |
| 4 | GitHub API failure | Check authentication and partial effects before retrying |
| 5 | Invalid arguments | Inspect command help and correct the invocation |
| 6 | Multiple stacks match | Switch to a non-shared branch |
| 7 | Rebase in progress | Resolve and continue, or abort the existing rebase |
| 8 | Stack locked | Wait for the other writer, then retry; lock timeout is five seconds |
| 9 | Stacked PRs unavailable | Report that the repository must enable stacks |
| 10 | Interrupted modify | Use `gh stack modify --abort` to restore the pre-modify state |

This skill uses `unstack`/`init` for restructuring, not `modify`. Remote selection,
linear stacks, and ambiguous shared branches are covered by
[operation contracts](operation-contract.md). Command-specific publication and
checkout effects are in [commands](commands.md); read the relevant section.

## Handle rebase conflicts

A code-3 exit from `sync` already rolled back its attempted rebases. Start
`gh stack rebase` to enter resumable recovery. Inspect the reported conflicts,
resolve them, stage the resolved paths, and run `gh stack rebase --continue`.
Repeat for later conflicts. If recovery cannot proceed, `gh stack rebase --abort`
restores all branches to their pre-rebase state.
