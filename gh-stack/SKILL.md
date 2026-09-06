---
description: Use to create, navigate, push, rebase, sync, restructure, or merge dependent branches and stacked PRs with gh-stack. Not for reviewing a single PR.
metadata:
    author: github
    github-path: skills/gh-stack
    github-ref: refs/tags/v0.1.0
    github-repo: https://github.com/github/gh-stack
    github-tree-sha: c95c8b5b4dd850f3fef007b304428f5684f2fb87
    version: 0.0.9
name: gh-stack
---
# gh-stack

Keep dependencies in lower branches and consumers above them; each PR compares
one layer against the branch below it. Branch names are passed literally, including
the repository-required prefix. Stage deliberate changes with ordinary git add/commit.

Before mutation, read [operation contracts](references/operation-contract.md).
For inspection, require installed/authenticated gh and its gh-stack extension; read
that reference if setup or remote selection is unresolved. Read
[output and recovery](references/recovery.md) before interpreting nonzero exits or
unsupported cases. Do not guess extension semantics from ordinary Git.

- Inspect with `gh stack view --json`; never launch its TUI.
- Supply branch/PR arguments to init, add, and checkout, and `--auto` to submit.
- Fix lower-layer code on that branch, then rebase upstack before continuing.
- For a mutation, read only the relevant command section in
  [commands](references/commands.md). Confirm the installed command's help when
  flags or behavior are uncertain; the catalog records its source version.
- Before removing/reordering/renaming stack layers, read
  [restructuring](references/restructure.md).
- Stack merging uses `gh stack merge --yes`, with the requested scope and method,
  only when merging is authorized. An instruction about command syntax grants no
  additional authority to merge, prune, or force-push.
