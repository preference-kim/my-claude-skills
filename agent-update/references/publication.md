## Validate and publish

This workflow publishes only the personal dotfiles and skill repositories. The
configured development checkout is an installation target: verify that its tracked
files and ordinary untracked state remain unchanged. A project contribution
requires an explicit request for that destination and a separate project workflow.

Repository ownership does not establish permission to disclose its contents.
Before any publication, verify the destination's visibility and authorized audience,
then inspect every outgoing file, historical object, commit message, PR body, and
comment for confidential project information. Internal audits, evaluation fixtures
and results, logs, installation inventories, and incident evidence remain outside
both worktrees under the local agent-update state directory. Publish only content authorized for that specific audience; do not
infer consent from a personal account, private repository, or prior push request.

During a suspected exposure, stop publication, preserve necessary evidence outside
Git, and prepare local cleanup. Keep remediation within the user-authorized scope; do not change repository
visibility or unrelated history without authorization. A local deletion or new deletion
commit does not establish removal from GitHub history, PR refs, caches, or copies.
Report verified removal separately from remaining access and unresolved checks.

1. Re-read every changed instruction or skill file and remove duplication, stale paths, and chronological patchwork.
2. Run `git diff --check` in both repositories. Run the installed skill validator when available and verify the required SKILL.md frontmatter directly otherwise. Re-run the full instruction-link and skill manifest comparison for the current host's configured mode after link repair.
3. Read `<dotfiles>/PUBLICATION.md`, then run
   `python3 <dotfiles>/scripts/publication-guard.py install` to install or verify
   both repositories' commit and push guards without discarding existing hooks.
   Review both diffs and stage only exact, disclosure-reviewed files. New files
   require explicit entries in that repository's `.publication-policy.json`;
   never populate it from an untracked directory inventory. Keep the historical
   base unchanged during routine maintenance. Run the guard's `index` check in
   each repository before committing and its `history HEAD` check before pushing.
   For a changed user-owned nested skill repository, validate, commit, and push
   its own `main` first; verify remote reachability before recording its pointer.
   Never publish a parent whose gitlink names an unpublished child commit, and
   never push changes to a vendor-owned submodule as part of this exception.
4. Commit skills changes first with a concise message and no co-author. Commit the dotfiles change second so its submodule pointer names that child commit.
5. Push the skills commit to `origin/main`. Confirm it is reachable from the remote branch, then push dotfiles to `origin/main`. Do not create a feature branch or pull request for these personal agent-file updates.
6. If the child push succeeds but the parent push fails, report both commit IDs. Retry the parent only when the remote remains an ancestor of the local commit; otherwise stop without rewriting history.
7. Write today's date and the reviewed upstream commit to `last-successful-sync` only after both pushes succeed or when no tracked change was needed, completed workspace cleanup succeeds, the current host's configured entry points and complete skill manifest pass verification, and no installed CLI remains known to be outdated. If cleanup fails, the host is unconfigured, or a known-outdated CLI could not be updated and verified, do not write `last-successful-sync` for this refresh.
8. Re-read the final AGENTS.md and SKILL.md for the current session. Report changed files, commit IDs, push results, the host's configured mode and resolved `moreh_dev_root` when applicable (or its unconfigured state), repaired links, each CLI's before/after version and update outcome, any required process restart, and any verification limitation. Keep a no-change daily refresh unobtrusive.

Never commit secrets, credentials, caches, histories, state files, or unrelated local settings.
