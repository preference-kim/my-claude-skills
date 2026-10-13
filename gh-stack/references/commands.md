# Command contracts

Read only the section for the operation. The skill metadata records a source
revision. If installed behavior is uncertain, inspect command help.
The [operation contracts](operation-contract.md) own prerequisites, remote selection,
and authorization.

## Initialize: `gh stack init --base <trunk> <branches...>`

Provide at least one branch in bottom-to-top order. Without arguments, `init`
prompts. `--base` (also `-b`) defaults to the repository's default branch.
Existing branches are adopted, missing branches are created from trunk, and the
last listed branch is checked out. Names are literal. `init` enables rerere,
which requires the operation contract's preconfiguration to avoid prompting.

## Add: `gh stack add <branch>`

Run from the topmost branch, or trunk when the stack is empty. Otherwise it exits
with code 5. Pass a name to avoid prompting. Uncommitted changes carry into the
new branch, so first commit or stash work that belongs to the current branch.
Use ordinary Git to stage deliberate changes and commit.

If using the combined commit shortcut, `-m <message>` accepts either `-A` for all
changes including untracked files or `-u` for tracked changes. These flags require
`-m` and are mutually exclusive. If the current branch has no commits, `add -Am`
commits on that branch instead of creating a new one. Omitting a name with `-m`
generates a date/slug name, so supply the repository-compliant name explicitly.

## Push: `gh stack push`

Pushes active branches, excluding merged and queued branches, using explicit
per-branch `--force-with-lease` in one non-atomic multi-ref push. Some refs can
succeed while another is rejected. Inspect the actual partial result, repair the
rejected branch, and rerun. This command does not create or update PRs.

## Submit: `gh stack submit --auto`

Always pass `--auto` to avoid title prompts. `--open` marks new and existing PRs
ready for review. Pushes active branches sequentially with explicit per-branch
`--force-with-lease`. The operation is not atomic: earlier pushes and PR changes
remain after a later rejection. Inspect that state, repair, then rerun.

Creates missing PRs against the first non-merged ancestor and syncs existing PR
metadata, then links the stack on GitHub. A completed stack cannot be extended.
If all its PRs merged, unmerged branches become a new stack rooted at trunk.
Code 9 means stacked PRs are unavailable; non-interactive submission cannot choose
the interactive fallback to ordinary PRs.

Titles and bodies are automatic: one commit supplies its subject/body, while
multiple commits produce a humanized branch-name title. There is no custom-body
flag. Use `write-technical-pr` before an authorized `gh pr edit`, preserving stack
metadata/footer.

## Link: `gh stack link <branch-or-pr> <branch-or-pr> [...]`

Use bottom-to-top order and at least two entries, or an existing stack number
followed by entries to append. A numeric first argument resolves as an existing
stack first, then PR or branch. Other numeric arguments try PR numbers before
branch names. Existing entries in the target stack are skipped; entries in a
different stack are rejected.

`--base <branch>` selects the bottom base, defaulting to the repository default.
`--open` marks new and existing PRs ready. Branch arguments are pushed atomically
without force. Missing PRs are created with generated titles and chained bases;
existing PR bases are corrected. Stack updates are additive and never remove
existing entries. This command does not create or modify local tracking state.

## Sync: `gh stack sync`

Fetches and reconciles the remote stack, imports newly added branches, fast-forwards
trunk if possible, and cascade-rebases when trunk moved, handling merged PRs.
Diverged trunk produces
a warning. A rebase conflict restores all branches to their pre-rebase state and
exits 3; use the [resumable recovery workflow](recovery.md#handle-rebase-conflicts).

Next it pushes active branches atomically, syncs PR state, and creates or updates
an additive stack object when at least two PRs exist. It never opens missing PRs.
In non-interactive use, local merged branches are pruned only with `--prune`.

Local/remote stack divergence aborts non-interactively. `Sync aborted` can return
exit code 0 without synchronization. Check the message and resulting stack state
before claiming completion.

## Rebase: `gh stack rebase [branch]`

Fetches and cascade-rebases, targeting the current branch by default.
`--downstack` limits trunk-to-target scope; `--upstack` limits target-to-top scope.
`--no-trunk` skips fetching and trunk updates, rebasing only between stack layers.
Merged PRs use `--onto` to replay onto the merge target. Rerere can reuse earlier
conflict resolutions.

For conflicts, follow [recovery](recovery.md#handle-rebase-conflicts): stage resolved
paths and run `gh stack rebase --continue`; `--abort` restores all branches.

## Inspect and navigate

`gh stack view --json` sends data to stdout; omitting `--json` launches a TUI.
The object includes `trunk`, `currentBranch`, and `branches`. Each branch has
`name`, `head`, `base` (parent head at last sync), `isCurrent`, `isMerged`,
`isQueued`, and `needsRebase` (base is not an ancestor). Optional `pr` has number,
URL, and state (`OPEN`, `MERGED`, or `QUEUED`).

Use `up [count]`, `down [count]`, `top`, `bottom`, or `trunk` for navigation.
Counts default to one and clamp at stack bounds. Navigation from active branches
skips merged branches; `bottom` selects the first non-merged branch above trunk.

## Checkout: `gh stack checkout <stack-number|pr-number|pr-url|branch>`

Always pass an argument. Bare numbers resolve as stack number, then PR number,
then branch. A stack/PR number or PR URL fetches the GitHub stack and its branches
and sets up local tracking. A branch name searches only local stacks.

Different local/remote branch compositions trigger a conflict prompt with no
bypass flag. Record local tracking, then use `gh stack unstack --local` to remove
that conflicting grouping before retrying checkout. This leaves GitHub grouping,
branches, and PRs intact. Do not discard branch work to resolve tracking.

## Unstack: `gh stack unstack [stack-number] [--local]`

Removes grouping/tracking, never branches or PRs. With no number, targets the
active stack locally and on GitHub. A stack number removes that grouping through
the GitHub API from anywhere in the repository, plus its local tracking if present.
An unknown remote number exits 2.

`--local` never contacts GitHub. A number with `--local` must be tracked locally.
Before structural changes, read [restructuring](restructure.md).

## Merge: `gh stack merge [pr-or-stack-number] --yes`

Use only for an authorized merge. `gh pr merge` does not support stacked PRs.
With no scope argument, this merges the entire stack bottom-to-top. A PR number
limits scope through that PR; a stack number needs no local checkout.
Choose `--squash`, `--rebase`, `--merge`, or `--merge-method <method>`; otherwise
the last-used method applies.

Direct stack merge is all-or-nothing and reports any blocking PR. The client
checks basic open/non-draft state; it does not support bypassing merge requirements.
For a base with a merge queue, the stack is queued together. The queue chooses the
method, ignores a supplied method with a warning, and can land PRs in separate
groups. Do not report queue entry as a completed merge.
