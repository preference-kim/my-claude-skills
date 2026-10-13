# Restructure a stack

Before removing, reordering, or renaming layers, record the current branch order
and intended replacement. Apply the operation and `unstack` command contracts.
`gh stack unstack` removes local tracking and GitHub grouping, not branches or PRs.
Then make the authorized structural changes and run
`gh stack init --base <trunk> <branches-in-new-order...>`.

Use `unstack --local` only when GitHub grouping must remain intact, such as replacing
conflicting local tracking before checkout. Branch deletion and remote grouping
changes require their own authorized scope; unstacking does not grant it.
