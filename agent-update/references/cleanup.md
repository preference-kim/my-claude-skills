## Clean completed workspace artifacts

Perform this cleanup during every daily, forced, or requested refresh, including a same-day daily refresh that skips network and repository work.

1. Inspect the home-directory top level and known reviewer temporary/cache roots for abandoned review outputs, temporary directories, diagnostic scratch, and other agent-created transient artifacts. Also identify completed experiment outputs or datasets whose producing session no longer needs them.
2. Enumerate every cleanup target as an exact canonical path. Before deletion, require that each target is owned by the current user, is not a symlink, is not a Git repository or worktree, is not referenced by a live process, and is not a credential or configuration directory, shared default asset, active input, or evidence still needed to reproduce a current conclusion. Never delete through a broad home-directory glob, follow a symlink, or infer ownership for an ambiguous path.
3. Remove unambiguous abandoned review and temporary artifacts without asking. Prefer a recoverable trash operation when it is available and preserves the intended space reclamation; otherwise delete only the individually verified targets.
4. Ask whether the user wants to retain completed experiment data, explicitly stating that deletion is the default. Delete it unless the user requests retention. If the user does not answer or the completed scope is unclear, preserve it and report the unresolved cleanup item.
5. Report the exact categories removed, the measured space reclaimed, any retained experiment data, and whether recovery is possible. An unexpected cleanup failure is a refresh failure: report its current impact and do not write the successful-sync stamp.
