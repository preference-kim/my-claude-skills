### Restructure a stack (remove a branch, reorder, or rename)

Use `unstack` to tear down the stack, make structural changes, then re-init:

```bash
# 1. Remove the local tracking and the GitHub stack grouping (PRs are NOT deleted)
gh stack unstack

# 2. Make structural changes — e.g. delete a branch, reorder, rename
git branch -m old-branch-1 new-branch-1

# 3. Re-create the stack with the new structure
gh stack init --base main new-branch-1 new-branch-2 new-branch-3
```

---
