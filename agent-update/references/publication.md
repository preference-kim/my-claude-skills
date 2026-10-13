# Validate and publish

Read `<dotfiles>/PUBLICATION.md` before preparing outgoing changes. It owns
disclosure review, publication guards and exposure handling. This workflow
publishes only personal dotfiles/skills repositories; the configured development
checkout receives ignored links and must retain its tracked/ordinary untracked
status. A project contribution requires its own authorized workflow.

1. Re-read changed guidance for purpose, preserved requirements, reference
   reachability and contradictions. Complete `skill-maker`'s requirement and
   behavior checks for harness/skill edits.
2. Run `git diff --check` in both repositories. Validate every changed
   `SKILL.md`, including behind moved submodule pointers, against the
   [Agent Skills specification](https://agentskills.io/specification), not a
   vendor validator's different field list:
   - YAML permits only `name`, `description`, `compatibility`, `license`,
     `metadata`, `allowed-tools`.
   - Required `name`: 1–64 lowercase letters/digits/hyphens, no leading,
     trailing or consecutive hyphens, equal to its directory name.
   - Required `description`: 1–1024 characters.
   - Optional `compatibility`: 1–500 characters; `metadata`: string keys/values.
   No changed skill means no frontmatter check. After link repair, verify the
   host's complete instruction/source/scope manifests again.
3. Install/verify both repository guards with
   `python3 <dotfiles>/scripts/publication-guard.py install`, preserving hooks.
   Stage only exact disclosure-reviewed files; new files need exact approved
   `.publication-policy.json` entries, never an untracked-directory inventory.
   Keep the historical base unchanged. Run each guard's `index` check before
   commit and `history HEAD` before push.
4. Publish any changed user-owned nested skill on its own `main` first and
   verify remote reachability before recording its gitlink. Vendor submodules
   remain at approved commits. Commit skills before dotfiles with concise
   messages and no co-author. Push skills to `origin/main`, verify reachability,
   then push dotfiles to `origin/main`; use no feature branch/PR. No parent may
   name an unpublished child.
5. If a child push succeeds but the parent fails, report both IDs. Retry only
   while the parent remote remains an ancestor; otherwise stop without rewriting
   history.
6. Stamp today's local date and reviewed upstream commit in
   `last-successful-sync` only when pushes succeeded (or no tracked change was
   needed), cleanup passed, configured entry points and complete manifest/
   frontmatter checks passed, and no installed CLI remains known outdated.
   Unconfigured hosts, required failures and unverified known-outdated updates
   block it. Routine SSH reports separately and does not gate this stamp;
   explicitly requested other private payloads follow
   [private synchronization](private-sync.md)'s combined-request success rule.
7. Re-read final AGENTS/skill for this session. Report changed files, commit/push
   results, configured mode/root or unconfigured state, link repairs, CLI
   before/after versions/outcomes, required restart and verification limits.
   Keep no-change daily refreshes unobtrusive.

Caches, histories, state, credentials and unrelated settings are not outgoing
harness content.
