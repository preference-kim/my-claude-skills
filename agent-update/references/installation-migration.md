# Migrate a legacy installation

Read [installation](installation.md) before either migration below. These paths
do not run for an already canonical layout.

## Discovery-root clone

Inspect the root's status and recursive submodules. Automatic refresh may
migrate only a clean clone. A dirty clone requires explicit authorization to
preserve and migrate that exact installation; one such request creates no future
permission.

Verify exact canonical path, ownership, nested Git metadata and live-process
working-directory/input use; defer active or ambiguous targets. Save the entire
root, including Git metadata and modified/untracked files, below a unique
timestamped `${XDG_STATE_HOME:-$HOME/.local/state}/agent-update/backups/` directory. Record inventory,
original location, link targets and project exclude block outside public Git.
Verify backup contents and nested repository access before replacing entries;
keep it until retention is resolved.

Recreate real discovery roots and restore unrelated/provider entries at their
original paths with contents/targets preserved. Canonical-name real entries
remain overrides unless replacement was explicitly authorized. Back up replaced
versions; do not merge them into vendor sources or revive retired skills. On
failure, remove only newly created managed entries and restore the saved root
and exclude block without overwriting concurrent edits. Verify replacement
entries/references before old-link cleanup.

## Former development-server shell fragment

When a registered development server's `~/.bashrc` sources the former untracked
`~/.config/moreh-dev/shell.bash`, back up both files under
`${XDG_STATE_HOME:-$HOME/.local/state}/agent-update/backups/`. Replace only that
source line with the tracked dotfiles line, append old fragment lines absent
from the tracked fragment (for example personal aliases) to `~/.bashrc`, and
remove `shell.bash`. Verify a new interactive shell starts without errors.
