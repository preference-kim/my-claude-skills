## Resolve the installation manifest

Require a valid host-local `mode` before changing any entry point. An absent or
invalid mode blocks all installation; do not infer one. A missing or invalid
`moreh_dev_root` blocks only project installation: continue user-scope skills,
report the project failure, and withhold the successful-sync stamp.

Build the source manifest from Git-tracked top-level `*/SKILL.md` files and
explicitly configured top-level gitlinks. For a gitlink, resolve its optional
`skill-path` in `.gitmodules` from the submodule root; the default is `.`.
Require an initialized submodule and a readable `SKILL.md` at that source.
Reject absolute paths and paths that resolve outside the submodule. Keep the
top-level directory name as the manifest key and require it to match the skill
name. Require each source file or gitlink in `.publication-policy.json`.
Never enumerate ignored or untracked sources into this manifest.

`simple-english` uses `skill-path = skills/simple-english`. Keep its upstream
files unchanged and install only that skill directory. Its plugin, session hooks,
and output style are separate upstream capabilities, not part of skill installation.

Read `<skills>/.installation-policy.json` as the single installation-scope map:
each key is an exact source skill directory name and each value is `user` or
`moreh-dev`. Reject duplicate keys, unknown values, missing classifications, and
keys absent from the source manifest before changing links. Publication approval
does not assign installation scope. Every manifest skill must be classified.

Resolve a discovered skill's symlink to its canonical directory before reading
relative references. Sibling resources such as `review-common` and personal
`agent-guidance` remain at their canonical locations; do not copy them into every
installation root or require a Moreh checkout for user-scope references.

## Install user-scope skills in both modes

Keep `~/.agents/skills` (Codex) and `~/.claude/skills` (Claude) as real directories.
For every `user` skill, maintain these individual symlinks:

- `~/.agents/skills/<name> -> <resolved-source-directory>`
- `~/.claude/skills/<name> -> <resolved-source-directory>`

The resolved source is `<dotfiles>/skills/<name>`, or its declared `skill-path`
for a vendor submodule. For SimpleEnglish it is
`<dotfiles>/skills/simple-english/skills/simple-english`.

Do this in both `host-global` and `moreh-dev`. Do not create duplicate project
entries for these skills. Do not clone the skills repository into a discovery
root or replace a root with a whole-directory symlink. Preserve `.system`,
provider-managed installations, and unrelated host-local entries.

Create missing parent directories. Leave correct links unchanged. Replace an
incorrect symlink only when its target belongs to the canonical or recorded prior
managed installation. Preserve unrelated or ambiguously owned links, including
dangling links, as reported overrides. Never replace a real file or directory
automatically: an instruction or root conflict blocks that installation; a real
per-skill item is an explicit local override to report while continuing the
remaining skills. Do not silently count an override as canonical.

## Install instructions and project-scope skills

### Mode `host-global`

Keep these instruction entry points:

- `~/.codex/AGENTS.md -> <dotfiles>/.codex/AGENTS.md`
- `~/.claude/CLAUDE.md -> <dotfiles>/.claude/CLAUDE.md`

Do not install `moreh-dev` skills globally. List them as intentionally excluded
from this mode's expected manifest, not as missing user skills. Do not search
for or change an unconfigured project checkout.

### Mode `moreh-dev`

This mode selects discovery locations, not a publication destination. Personal
sources stay in dotfiles/shared skills. Preserve tracked project skills; do not
reorganize or publish them during personal harness maintenance.

Use the exact canonical Git checkout validated by preflight. Keep these
project-local instruction links, without creating host-global instructions:

- `<moreh-dev-root>/AGENTS.md -> <dotfiles>/AGENTS.md`
- `<moreh-dev-root>/CLAUDE.md -> <dotfiles>/CLAUDE.md`

For only the `moreh-dev` skills, maintain:

- `<moreh-dev-root>/.agents/skills/<name> -> <resolved-source-directory>`
- `<moreh-dev-root>/.claude/skills/<name> -> <resolved-source-directory>`

Use relative project symlinks derived from the resolved checkout locations.
Keep skill roots as real directories. Before creating or replacing any project
entry, require that its path is untracked. Preserve real per-skill entries as
reported project overrides; root and instruction conflicts block project
installation. Never overwrite tracked entries, even if they are symlinks.

Record the checkout's tracked and ordinary untracked status before and after.
Keep managed links ignored through a delimited block in the file returned by
`git -C <moreh-dev-root> rev-parse --git-path info/exclude`. Preserve all text
outside `# BEGIN agent-update managed links` and
`# END agent-update managed links`. List only exact repository-relative paths
that currently exist as managed symlinks; never use broad wildcards. Update the
block after creating or removing links. The checkout's ordinary status must
remain unchanged.

## Install the shell, Git and tmux environment

Link the tracked settings from dotfiles in both modes. Each link is additive:
create a missing startup file, add one line or entry, and never rewrite other
lines. Check the links on every refresh and write only when one is missing.
Later changes to the tracked files reach the host through the dotfiles pull.

On every host:

- `~/.gitconfig` must include `<dotfiles>/git/config`. If no include names it, insert
  `[include]` with `path = <dotfiles>/git/config` at the start of the file, so the
  file's own settings still take precedence. Report the effective user name and
  email (`git config user.email`; `--global` ignores includes) before and after; a
  change means a local value was missing, not overridden.
- Link `~/.tmux.conf` to `<dotfiles>/.tmux.conf` when it is absent or identical.
  Keep a different real file as a reported local override.

Link the shell settings only when the host's registration in
`~/.config/agent-update/private-sync.json` has `device_role: development-server`.
The shell fragment shows the server banner. A personal device, or a host without
a registration, gets no shell link. Leave its startup files unchanged, including
a line that already sources a dotfiles fragment.

- The login shell's startup file must source the dotfiles fragment: `~/.bashrc`
  sources `<dotfiles>/bash/bashrc` for bash, and `~/.zshrc` sources
  `<dotfiles>/zsh/interactive.zsh` for zsh. Any existing line that sources that path
  counts. Otherwise append `[ -r "<path>" ] && . "<path>"`.

On a development server, when `~/.bashrc` sources the former untracked
`~/.config/moreh-dev/shell.bash`, back up both files under the agent-update
`backups/` state directory. Replace that line with the dotfiles line, append the
old file's lines that the tracked fragment lacks (such as personal aliases) to
`~/.bashrc`, then remove `shell.bash`. Verify that a new interactive shell starts
without errors.

## Migrate legacy installations and remove obsolete links

A discovery root may be a legacy Git clone. Inspect its status and recursive
submodules before migration. Automatic refresh may migrate only a clean clone;
a dirty clone requires explicit authorization covering preservation and migration
of that exact installation. Do not turn a one-time authorized migration into a
general permission to move dirty repositories.

Before moving a root, verify its exact canonical path, ownership, nested Git
metadata, and live-process working-directory/input references. Defer any active
or ambiguous target. Save the complete root, including Git metadata, modified
and untracked files, under a unique timestamped directory below
`${XDG_STATE_HOME:-$HOME/.local/state}/agent-update/backups`. Record its inventory,
original location, link targets, and original project exclude block outside the
public repositories. Verify backup content and nested repository accessibility
before replacing discovery entries. Keep the backup until retention is resolved.

Recreate real discovery roots. Restore unrelated host-local and provider-managed
entries at their original paths, preserving contents and symlink targets. For
canonical-name collisions, preserve real entries as overrides unless the user
explicitly authorized canonical replacement of those entries. Keep replaced
versions in the backup; do not merge them into vendor sources or revive retired
skills. On failure, remove only newly created managed entries and restore the
saved root and exclude block without overwriting concurrent changes.

For each relocated skill, verify its replacement entries and references before
removing its old links. Defer relocation cleanup when its required destination
cannot be installed, including an invalid project root. Intentionally excluded
or retired skills require no replacement. Remove obsolete per-skill symlinks only when their resolved target is a canonical skill below
`<dotfiles>/skills`, their path is untracked, and that location is no longer in
the current expected installation. This includes old Codex `.codex/skills`
links, project copies of user skills, and global copies of project-only skills.
Also remove managed links whose source has left the approved manifest. Never
remove real entries or links to unrelated targets. Do not remove the supported
`~/.agents/skills` entries as legacy links.

## Verify the complete installation

Compare every expected entry, not selected names, with the source and scope
manifests. Require a canonical link and readable `SKILL.md`, or an explicitly
reported local/project override. Verify canonical reference paths, instruction
links, absence of obsolete managed duplicates, and unchanged project status.
A second synchronization must make no changes. A failed required installation
or unresolved conflict prevents a successful-sync stamp; an intentionally
excluded scope does not. Missing runtime discovery checks must be reported as
unverified, not described as successful live discovery.
