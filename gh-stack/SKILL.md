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

Arrange layers by dependency: foundations below consumers, with each PR based on
the branch below. Fix lower-layer code there, then `gh stack rebase --upstack`
before continuing above. Use deliberate ordinary Git staging and commits.

Run non-interactively. Inspect with `gh stack view --json`, never its TUI.
Before mutation, read [operation contracts](references/operation-contract.md)
and only the relevant section of [commands](references/commands.md). For read-only
inspection, load the operation contracts only if installation, authentication, or
remote selection is unresolved. Confirm installed command help when uncertain.

Before removing, reordering, or renaming layers, read
[restructuring](references/restructure.md). For nonzero exits, cancellation, or
unsupported cases, read [recovery](references/recovery.md) before choosing a response.
Do not infer extension behavior from ordinary Git or report success from exit
status alone.
