## Maintain the configured entry points and skill installations

If the current host has no usable configuration (see steps 4-5 of "Resolve the repositories"), do not create, remove, or repair any entry point below `~/.codex`, `~/.claude`, or a possible development checkout. Report the missing or invalid field, point to `agent-file-sync.example.yaml`, and stop this part of the refresh.

### Mode `host-global`

Keep these host-global instruction entry points:

- `~/.codex/AGENTS.md -> <dotfiles>/.codex/AGENTS.md`
- `~/.claude/CLAUDE.md -> <dotfiles>/.claude/CLAUDE.md`

Keep `~/.codex/skills` and `~/.claude/skills` as real directories so host-local and shared skills can coexist. Do not clone the shared skills repository into either location and do not replace either directory with a whole-directory symlink.

Build the shared skill manifest from Git-tracked top-level `*/SKILL.md` files
and explicitly configured top-level gitlinks whose initialized submodules contain
`SKILL.md`. Require each source path or gitlink in `.publication-policy.json`.
Do not enumerate ignored or untracked directories: local presence does not make
a skill part of the shared installation. For each approved skill, maintain both
tool-specific entries:

- `~/.codex/skills/<name> -> <dotfiles>/skills/<name>`
- `~/.claude/skills/<name> -> <dotfiles>/skills/<name>`

Create missing parent directories. Leave correct links unchanged and replace an incorrect symlink. Never replace a real file or directory. For an instruction entry point or skill-directory root, stop and report the conflict. For a per-skill entry, preserve a real host-local item as an override, report it as skipped, and continue with the remaining skills.

A tool skill directory may be a legacy clone of the shared skills repository. Migrate it only when its tracked files and recursive submodules are clean: move the clone to a timestamped directory below `${XDG_STATE_HOME:-$HOME/.local/state}/agent-update/backups`, recreate the tool skill directory, preserve untracked entries whose names are neither repository metadata nor canonical skill names, and then create the managed links. Leave the backup in place and report it. Stop if local changes, nested-repository changes, or an ambiguous name collision make ownership unclear.

Remove a stale per-skill symlink only when its resolved target is below `<dotfiles>/skills` and that source skill is absent from the tracked manifest. After both tool-specific entries are verified, remove obsolete symlinks below `~/.agents/skills` that resolve to the same shared skills; do not touch real entries or unrelated links.

Verify the installation as a manifest comparison, not by checking selected names: every source skill must resolve through both tool directories to the canonical directory and a readable `SKILL.md`, or be listed as an explicit host-local override. A refresh is not successful while a source skill is silently missing from either tool.

### Mode `moreh-dev`

This mode selects a discovery location, not a publication destination. Personal
sources remain in dotfiles/shared skills; installation changes only ignored links
and the exact local exclude metadata. Preserve tracked project skills. Do not
reorganize or publish them as part of personal harness maintenance.

Let `<moreh-dev-root>` denote the canonical Git checkout root resolved from this host's `moreh_dev_root`. Do not create or repair host-global entries below `~/.codex` or `~/.claude` in this mode. Keep these project-local instruction entry points:

- `<moreh-dev-root>/AGENTS.md -> <dotfiles>/AGENTS.md`
- `<moreh-dev-root>/CLAUDE.md -> <dotfiles>/CLAUDE.md`

Use relative symlink targets derived from the resolved repository locations so moving the checkouts together preserves the links. Before creating either link, require that the destination path is not tracked by the configured checkout. Leave a correct link unchanged and replace an incorrect symlink. Never replace a real file or directory; report the conflict and stop project synchronization.

Keep `<moreh-dev-root>/.codex/skills` and `<moreh-dev-root>/.claude/skills` as real directories so project-owned and shared skills can coexist. Do not replace either directory with a whole-directory symlink. Use the tracked, publication-approved shared skill manifest defined above; ignored or untracked sources must not enter discovery. For each source skill, maintain both project entries as relative links to the canonical skill directory:

- `<moreh-dev-root>/.codex/skills/<name> -> <dotfiles>/skills/<name>`
- `<moreh-dev-root>/.claude/skills/<name> -> <dotfiles>/skills/<name>`

Create a missing tool skill directory only when neither a file nor a symlink occupies that path. Before creating a per-skill link, require that the destination path is not tracked by the configured checkout. Leave a correct link unchanged and replace an incorrect symlink. Preserve a real file or directory as a project-owned override, report it as skipped, and continue with the remaining skills.

Remove a stale per-skill symlink only when its resolved target is below `<dotfiles>/skills` and that source skill is absent from the tracked manifest. Do not touch real entries, tracked entries, or links to any other location.

Keep managed links out of the configured checkout's Git status through a delimited block in the file returned by `git -C <moreh-dev-root> rev-parse --git-path info/exclude`. The block must start with `# BEGIN agent-update managed links` and end with `# END agent-update managed links`. Preserve all content outside the block. Within it, list only the repository-relative paths that currently exist as managed symlinks; update the block after link creation or removal, and never use a broad wildcard that could hide project-owned files.

Verify project installation as a manifest comparison, not by checking selected names: both instruction links must resolve to their canonical dotfiles files, and every source skill must resolve through both project tool directories to the canonical directory and a readable `SKILL.md`, or be listed as an explicit project-owned override. Record the configured checkout's status before and after synchronization and require that its tracked and ordinary untracked state is unchanged; the managed ignored links must be the only local metadata added. A refresh is not successful while a required project entry is silently missing.
