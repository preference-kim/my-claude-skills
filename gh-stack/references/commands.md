# Command reference

## Commands

### Initialize a stack — `gh stack init`

Creates a new stack. **Always provide at least one branch name as a positional argument** — running without branch arguments triggers interactive prompts that agents cannot use.

```
gh stack init [flags] <branches...>
```

```bash
# Create a stack with a new branch
gh stack init auth
# → creates auth and checks it out

# Create a stack with new branches
gh stack init branch-a branch-b branch-c

# Use a different trunk branch
gh stack init --base develop branch-a branch-b

# Adopt existing branches into a stack (handled automatically if the branches exist)
gh stack init branch-a branch-b branch-c
```

| Flag | Description |
|------|-------------|
| `-b, --base <branch>` | Trunk branch (defaults to the repo's default branch) |

**Behavior:**

- Branch names are created exactly as given (slashes are allowed and kept as-is)
- Creates any branches that don't already exist (branching from the trunk branch)
- Existing branches are adopted automatically; missing branches are created from the trunk
- Checks out the last branch in the list
- Enables `git rerere` so conflict resolutions are remembered across rebases. On first run in a repo, this may trigger a confirmation prompt — pre-configure with `git config rerere.enabled true` to avoid it

---

### Add a branch — `gh stack add`

Add a new branch on top of the current stack. Must be run while on the topmost branch (or the trunk if the stack has no branches yet). **Always provide a branch name** — running without one triggers an interactive prompt.

```
gh stack add [flags] <branch>
```

**Recommended workflow — create the branch, then use standard git:**

```bash
# Create a new branch and switch to it
gh stack add api-routes

# Write code, stage deliberately, and commit
git add internal/api/routes.go internal/api/handlers.go
git commit -m "Add user API routes"

# Make more commits on the same branch as needed
git add internal/api/middleware.go
git commit -m "Add rate limiting middleware"
```

**Shortcut — stage, commit, and branch in one command:**

```bash
# Create a new branch, stage all changes, and commit
gh stack add -Am "Add API routes" api-routes

# Create a new branch, stage tracked files only, and commit
gh stack add -um "Fix auth bug" auth-fix
```

| Flag | Description |
|------|-------------|
| `-m, --message <string>` | Create a commit with this message |
| `-A, --all` | Stage all changes including untracked files (requires `-m`) |
| `-u, --update` | Stage tracked files only (requires `-m`) |

**Behavior notes:**

- `-A` and `-u` are mutually exclusive.
- When the current branch has no commits (e.g., right after `init`), `add -Am` commits directly on the current branch instead of creating a new one.
- **Branch names are used verbatim.** `gh stack add refactor/foo` creates a branch named `refactor/foo` — names are never prefixed or transformed. When `-m` is given without a branch name, the name is auto-generated from the commit message in date+slug format (e.g., `03-24-add_api_routes`).
- If called from a branch that is not the topmost in the stack, exits with code 5: `"can only add branches on top of the stack"`. Use `gh stack top` to switch first.
- **Uncommitted changes:** When using `gh stack add branch-name` without `-Am`, any uncommitted changes (staged or unstaged) in your working tree carry over to the new branch. This is standard git behavior — the working tree is not touched. Commit or stash changes on the current branch before running `add` if you want a clean starting point on the new branch.

---

### Push branches to remote — `gh stack push`

Push active stack branches to the remote.

```
gh stack push [flags]
```

```bash
# Push all branches
gh stack push

# Push to specific remote
gh stack push --remote upstream
```

| Flag | Description |
|------|-------------|
| `--remote <name>` | Remote to push to (use if multiple remotes exist) |

**Behavior:**

- Pushes all active (non-merged, non-queued) branches in one non-atomic multi-ref push with explicit per-branch `--force-with-lease` checks
- Some branches may update if another is rejected; fix the rejected branch and rerun the command
- Does **not** create or update pull requests — use `gh stack submit` for that

**Output (stderr):**

- `Pushed N branches` summary

---

### Submit branches and create PRs — `gh stack submit`

Push all stack branches and create PRs on GitHub. **Always pass `--auto`** — without it, `submit` prompts for a PR title for each new branch.

```bash
# Submit and auto-title new PRs (required for non-interactive use)
gh stack submit --auto

# Submit and create PRs as ready for review (not drafts)
gh stack submit --auto --open
```

| Flag | Description |
|------|-------------|
| `--auto` | Auto-generate PR titles without prompting (**required** for non-interactive use) |
| `--open` | Mark new and existing PRs as ready for review |
| `--remote <name>` | Remote to push to (use if multiple remotes exist) |

**Behavior:**

- Pushes each active (non-merged, non-queued) branch sequentially with explicit per-branch `--force-with-lease` checks; the overall submit is not atomic
- If a later branch push is rejected, earlier branch pushes and PR updates remain; fix the rejection and rerun the same command
- Creates a new PR for each branch that doesn't have one (base set to the first non-merged ancestor branch)
- After creating PRs, links them together as a **Stack** on GitHub (requires the repository to have stacks enabled)
- If every PR in the stack has already been merged, the stack is complete and can't be extended. `submit` automatically forks your unmerged branches into a **new** stack rooted at the trunk and creates it on GitHub, leaving the merged stack untouched.
- If stacks are not available (exit code 9), the repository does not have stacked PRs enabled. In interactive mode, `submit` offers to create regular (unstacked) PRs instead. In non-interactive mode, it exits with code 9.
- Syncs PR metadata for branches that already have PRs

**PR title auto-generation (`--auto`):**

- Single commit on branch → uses the commit subject as the PR title, commit body as PR body
- Multiple commits on branch → humanizes the branch name (hyphens/underscores → spaces) as the title

**Output (stderr):**

- `Created PR #N for <branch>` for each newly created PR
- `PR #N for <branch> is up to date` for existing PRs
- `Pushed and synced N branches` summary

---

### Link branches as a stack (no local tracking) — `gh stack link`

Link PRs into a stack on GitHub without creating any local tracking state. This is the recommended approach if you are managing stacked branches with other tools (jj, Sapling, git-town) and want to simply create GitHub Stacked PRs via an API.

```
gh stack link [flags] <stack-number | branch-or-pr> <branch-or-pr> [...]
```

```bash
# Link branches into a stack (pushes, creates PRs, creates stack)
gh stack link branch-a branch-b branch-c

# Use a different base branch and mark PRs as ready for review
gh stack link --base develop --open branch-a branch-b branch-c

# Link existing PRs by number
gh stack link 10 20 30

# Add branches to an existing stack of PRs
gh stack link 42 43 feature-auth feature-ui

# Append to the top of an existing stack by its stack number
# (7 is a stack number; only the new PRs/branches are listed)
gh stack link 7 48 feature-auth
```

When the first argument is a stack number, the remaining arguments are appended to the top of that stack, so you don't have to re-list its current PRs. Arguments already in the stack are skipped; arguments in a different stack are rejected. A numeric first argument is treated as a stack only when it matches an existing stack — otherwise it is a PR or branch.

| Flag | Description |
|------|---------|
| `--base <branch>` | Base branch for the bottom of the stack (defaults to the repository's default branch) |
| `--open` | Mark new and existing PRs as ready for review |
| `--remote <name>` | Remote to push to (use if multiple remotes exist) |

**Behavior:**

- Arguments are provided in stack order (bottom to top)
- Each argument can be a branch name or a PR number. Numeric arguments are tried as PR numbers first; if no PR with that number exists, the argument is treated as a branch name
- Branch arguments are pushed to the remote automatically (non-force, atomic)
- For branches without open PRs, new PRs are created with auto-generated titles and the correct base branch chaining (first branch uses `--base`, subsequent branches use the previous branch)
- Existing PRs whose base branch doesn't match the expected chain are corrected automatically
- If the PRs are not yet in a stack, a new stack is created. If some PRs are already in a stack, the stack is updated (additive only — existing PRs are never removed)
- Does **not** create or modify any local state

**Output (stderr):**

- `Pushing N branches to <remote>...`
- `Found PR #N for branch <name>` for branches with existing PRs
- `Created PR #N for <branch> (base: <base>)` for newly created PRs
- `Updated base branch for PR #N to <base>` when base branches are corrected
- `Created stack with N PRs` or `Updated stack to N PRs`

---

### Sync the stack — `gh stack sync`

Fetch, rebase, push, and sync PR state in a single command. This is the recommended command for routine synchronization.

```
gh stack sync [flags]
```

| Flag | Description |
|------|-------------|
| `--remote <name>` | Remote to fetch from and push to (use if multiple remotes exist) |
| `--prune` | Delete local branches for merged PRs |

**What it does (in order):**

1. **Fetch** latest changes from the remote
2. **Reconcile the remote stack** — mirror the GitHub stack locally. If PRs were added to the stack on GitHub, pull their branches down and append them to the local stack. If the local and remote stacks have diverged, aborts the sync in a non-interactive terminal. In an interactive terminal, offers prompts to resolve any divergence (replace local stack with remote version, delete stack on GitHub so it can be recreated, or cancel).
3. **Fast-forward trunk** to match remote (skips if already up to date, warns if diverged)
4. **Cascade rebase** all stack branches onto their updated parents (only if trunk moved). Handles merged PRs automatically. If a conflict is detected, **all branches are restored** to their pre-rebase state and the command exits with code 3 — see [Handle rebase conflicts](recovery.md#handle-rebase-conflicts-agent-workflow) for the resolution workflow
5. **Push** all active branches atomically
6. **Sync PR state** from GitHub and report the status of each PR
7. **Sync the stack object** — link the open PRs into a stack on GitHub. If the PRs are not yet in a stack, a new stack is created; if some PRs are already in a stack, it is updated (additive only). This only happens when two or more PRs exist. Sync **never opens PRs** — use `gh stack submit` for that
8. **Prune** — in interactive terminals, prompts to delete local branches for merged PRs. Use `--prune` to skip the prompt. In non-interactive environments, pruning only happens when `--prune` is passed explicitly

**Output (stderr):**

- `✓ Fetched latest changes from origin`
- `Pulling N new branches from the remote stack ...` then `✓ Pulled N new branches into the stack from the remote` (when the remote stack is ahead)
- `⚠ Your local stack has diverged from the stack on GitHub` (with `Local:` / `Remote:` chains) when the stacks have diverged
- `ℹ Sync aborted — no changes were made` when a sync is cancelled. Noninteractive
  divergence can return exit code 0 with this message; synchronization did not
  complete. Check the message and resulting stack state before reporting success.
- `✓ Trunk main fast-forwarded to <sha>` or `✓ Trunk main is already up to date`
- `✓ Rebased <branch> onto <base>` per branch (if base moved)
- `✓ Pushed N branches`
- `✓ PR #N (<branch>) — Open` per branch
- `Merged: #N, #M` for merged branches
- `✓ Stack created on GitHub with N PRs` / `✓ Stack updated on GitHub with N PRs` / `✓ Linked to the existing stack on GitHub` (when two or more PRs exist)
- `✓ Pruned <branch> (merged)` per pruned branch (when pruning)
- `✓ Stack synced` when the stack object on GitHub was created/updated to match local, or `✓ Branches synced` when only the branches were synced (fewer than two PRs or stacked PRs unavailable)

---

### Rebase the stack — `gh stack rebase`

Pull from remote and cascade-rebase stack branches. Use this when `sync` reports a conflict or when you need finer control (e.g., rebase only part of the stack).

```
gh stack rebase [flags] [branch]
```

```bash
# Rebase the entire stack
gh stack rebase

# Rebase only branches from trunk to current branch
gh stack rebase --downstack

# Rebase only branches from current branch to top
gh stack rebase --upstack

# Rebase stack branches without pulling from or rebasing with trunk
gh stack rebase --no-trunk

# After resolving a conflict: stage files with `git add`, then:
gh stack rebase --continue

# Abort and restore all branches to pre-rebase state
gh stack rebase --abort
```

| Flag | Description |
|------|-------------|
| `--downstack` | Only rebase branches from trunk to the current branch |
| `--upstack` | Only rebase branches from the current branch to the top |
| `--no-trunk` | Skip trunk — only rebase stack branches onto each other (no fetch, no trunk rebase) |
| `--continue` | Continue after resolving conflicts |
| `--abort` | Abort and restore all branches |
| `--remote <name>` | Remote to fetch from (use if multiple remotes exist) |

| Argument | Description |
|----------|-------------|
| `[branch]` | Target branch (defaults to the current branch) |

**Conflict handling:** See [Handle rebase conflicts](recovery.md#handle-rebase-conflicts-agent-workflow) for the full resolution workflow.

**Merged PR detection:** If a branch's PR was merged on GitHub, the rebase automatically handles this using `--onto` mode and correctly replays commits on top of the merge target.

**Rerere (conflict memory):** `git rerere` is enabled by `init` so previously resolved conflicts are auto-resolved in future rebases.

**No-trunk mode:** Use `--no-trunk` to skip fetching from the remote and rebasing with the trunk branch. Only inter-branch rebases are performed (branch 2 onto branch 1, branch 3 onto branch 2, etc.). Useful when you only need to align stack branches with each other without pulling upstream changes.

---

### View the stack — `gh stack view`

Display the current stack's branches, PR status, and recent commits. **Always pass `--json`** — without it, this command launches an interactive TUI that agents cannot operate.

```bash
# Always use --json
gh stack view --json
```

| Flag | Description |
|------|-------------|
| `--json` | Output stack data as JSON to stdout (**required** for non-interactive use) |

**`--json` output format:**

```json
{
  "trunk": "main",
  "currentBranch": "api-routes",
  "branches": [
    {
      "name": "auth",
      "head": "abc1234...",
      "base": "def5678...",
      "isCurrent": false,
      "isMerged": true,
      "isQueued": false,
      "needsRebase": false,
      "pr": {
        "number": 42,
        "url": "https://github.com/owner/repo/pull/42",
        "state": "MERGED"
      }
    },
    {
      "name": "api-routes",
      "head": "789abcd...",
      "base": "abc1234...",
      "isCurrent": true,
      "isMerged": false,
      "isQueued": false,
      "needsRebase": false,
      "pr": {
        "number": 43,
        "url": "https://github.com/owner/repo/pull/43",
        "state": "OPEN"
      }
    }
  ]
}
```

Fields per branch:
- `name` — branch name
- `head` — current HEAD SHA
- `base` — parent branch's HEAD SHA at last sync
- `isCurrent` — whether this is the checked-out branch
- `isMerged` — whether the PR has been merged
- `isQueued` — whether the PR is queued for merge (in a merge queue)
- `needsRebase` — whether the base branch is not an ancestor (non-linear history)
- `pr` — PR metadata (omitted if no PR exists). `state` is `"OPEN"`, `"MERGED"`, or `"QUEUED"`.

---

### Navigate the stack

Move between branches without remembering branch names. These commands are fully non-interactive.

```bash
gh stack up          # Move up one branch (further from trunk)
gh stack up 3        # Move up three branches
gh stack down        # Move down one branch (closer to trunk)
gh stack down 2      # Move down two branches
gh stack top         # Jump to the top of the stack (furthest from trunk)
gh stack bottom      # Jump to the bottom (first non-merged branch above trunk)
gh stack trunk       # Jump to the trunk branch (e.g. main)
```

Navigation clamps to stack bounds. Merged branches are skipped when navigating from active branches.

---

### Check out a stack — `gh stack checkout`

Check out a stack by stack number, pull request number, PR URL, or branch name. **Always provide an argument** — running `gh stack checkout` without arguments triggers an interactive selection menu.

```
gh stack checkout <stack-number | pr-number | pr-url | branch>
```

```bash
# By stack number (the identifier shown in the GitHub stack UI)
gh stack checkout 7

# By PR number (pulls from GitHub)
gh stack checkout 42

# By PR URL
gh stack checkout https://github.com/owner/repo/pull/42

# By branch name (local only)
gh stack checkout feature-auth
```

A bare number is resolved as a **stack number first** (the identifier shown in the GitHub stack UI); if no stack has that number it is tried as a PR number, then a branch name. When a stack or PR number (or PR URL) is provided, the command fetches the stack on GitHub, pulls the branches, and sets up the stack locally. If the stack already exists locally and matches, it switches to the branch.

> **⚠️ Agent warning:** If the local and remote stacks have different branch compositions, this command triggers an interactive conflict-resolution prompt that cannot be bypassed with a flag. To avoid this: run `gh stack unstack --local` first to remove the conflicting local tracking state (this keeps the stack on GitHub intact), then retry `gh stack checkout <pr-number>`.

When a branch name is provided, the command resolves it against locally tracked stacks only. This is always safe for non-interactive use.

---

### Remove a stack — `gh stack unstack`

Tear down a stack so you can restructure it — remove a branch, reorder branches, rename branches, or make other large changes. After unstacking, use `gh stack init` to re-create the stack with the desired structure.

Unstacking only removes the stack grouping (on GitHub and/or locally); it never deletes the underlying pull requests or branches.

With no argument, the command targets the active stack — the one containing the currently checked out branch — unstacking it on GitHub and removing local tracking.

Provide a stack number to unstack a specific stack on GitHub. This works from anywhere in the repository, whether or not the stack is checked out locally — the number is unstacked directly through the GitHub API (like `gh stack link`, no local tracking required). If the stack is also tracked locally, its local tracking is removed as well.

```
gh stack unstack [<stack-number>] [flags]
```

```bash
# Tear down the current stack — removes local tracking and the GitHub grouping (PRs are NOT deleted), then rebuild
gh stack unstack
gh stack init --base main branch-2 branch-1 branch-3 # reordered

# Unstack a specific stack by its number, from anywhere in the repo
gh stack unstack 7

# Only remove local tracking (keep the stack on GitHub)
gh stack unstack --local
```

| Flag | Description |
|------|-------------|
| `--local` | Only remove the stack locally (keep it on GitHub); never contacts GitHub |

> **Note for agents:** `gh stack unstack <number>` is a remote-first API wrapper — it unstacks on GitHub by number from anywhere in the repo, tracked locally or not, and is safe for non-interactive use. `--local` never contacts GitHub; combining `--local` with a number that isn't tracked locally is an error. An unknown stack number returns a "not found on GitHub" error (exit code 2).

---
