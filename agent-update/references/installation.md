# Install and verify canonical entry points

Use [preflight](preflight.md)'s validated host mode/root. Invalid mode blocks all
installation; an invalid project root blocks only project work and the success
stamp. Continue user-scope installation for a valid mode.

## Build the complete manifests

Source skills are Git-tracked top-level `*/SKILL.md` and approved top-level
gitlinks, each listed in `.publication-policy.json`. Never discover ignored or
untracked sources. For gitlinks, require initialization and readable `SKILL.md`
at `.gitmodules`' optional `skill-path` (default `.`), resolved inside the
submodule; reject absolute/escaping paths. The top-level directory remains the
manifest key and must match the skill name.

`<skills>/.installation-policy.json` assigns every source key exactly once to
`user` or `moreh-dev`. Reject duplicate/unknown/missing keys or values before
changing links. Publication approval does not assign scope. SimpleEnglish uses
`skills/simple-english` inside its submodule: preserve vendor files and install
that skill only, not its plugin, hooks or output style.

Resolve skill symlinks before relative references. Shared resources such as
`review-common` and `agent-guidance` stay at their canonical locations; user
skills must resolve them without requiring a development checkout.

## Install the configured layout

Keep real discovery directories with individual links to the resolved source
(`<dotfiles>/skills/<name>` or its declared nested `skill-path`).

| Scope | Codex | Claude |
| --- | --- | --- |
| User skills, both modes | `~/.agents/skills/<name>` | `~/.claude/skills/<name>` |
| Project skills, moreh-dev only | `<moreh_dev_root>/.agents/skills/<name>` | `<moreh_dev_root>/.claude/skills/<name>` |
| host-global instructions | `~/.codex/AGENTS.md -> <dotfiles>/.codex/AGENTS.md` | `~/.claude/CLAUDE.md -> <dotfiles>/.claude/CLAUDE.md` |
| moreh-dev instructions | `<moreh_dev_root>/AGENTS.md -> <dotfiles>/AGENTS.md` | `<moreh_dev_root>/CLAUDE.md -> <dotfiles>/CLAUDE.md` |

User skills have no duplicate project entries. In `host-global`, project skills
are intentionally excluded and unconfigured checkouts are untouched. In
`moreh-dev`, create no host-global instructions. Installation in a project does
not authorize publishing or reorganizing its tracked files.

Create missing parents and leave correct links unchanged. Replace a wrong
symlink only if its target belongs to the canonical or recorded prior managed
installation. Preserve unrelated/ambiguous links, including dangling ones, as
reported overrides. Real per-skill entries are local/project overrides; real
instruction/root conflicts block that installation. Do not silently count an
override as canonical. Preserve `.system`, provider-managed and unrelated entries;
do not replace discovery roots with whole-repository links/clones.

For project entries, require untracked paths before creation/replacement, even
for existing symlinks. Derive relative symlinks from resolved checkout locations.
Record tracked and ordinary untracked status before/after; it must remain
unchanged. Manage only exact existing managed-link paths within
`# BEGIN agent-update managed links` / `# END agent-update managed links` in
`git rev-parse --git-path info/exclude`; preserve outside text and update the
block after link creation/removal.

## Link the host environment

On every refresh, check additive links to tracked settings; write only missing
entries and preserve surrounding startup text. Tracked-file updates then arrive
through dotfiles pulls.

- Every host: prepend a missing `~/.gitconfig` include of
  `<dotfiles>/git/config` so local values retain precedence. Report effective
  `git config user.name` and `git config user.email` before/after; `--global`
  ignores includes. A change indicates an absent local value, not an override.
- Every host: link absent or identical `~/.tmux.conf` to
  `<dotfiles>/.tmux.conf`; keep a different real file as a reported override.
- Only a registered `development-server`: ensure the login shell's startup file
  sources the tracked fragment (`~/.bashrc` → `bash/bashrc`, `~/.zshrc` →
  `zsh/interactive.zsh`). Any existing source of that path counts; otherwise
  append `[ -r "<path>" ] && . "<path>"`. Personal/unregistered hosts' startup
  files remain unchanged, including existing dotfiles source lines.

Before migrating a legacy Git-clone discovery root or the former
`~/.config/moreh-dev/shell.bash`, read
[legacy migration](installation-migration.md). Do not automatically replace a
conflicting real root under routine link rules.

## Remove obsolete links and verify

Verify a relocated skill's destination entries/references before removing old
links. Defer removal when required installation is blocked, including a bad
project root. Intentionally excluded or retired skills need no replacement.
Remove only untracked managed symlinks whose resolved target is below
`<dotfiles>/skills` and whose location is no longer expected or source has left
the approved manifest. This covers old `.codex/skills` links, project user-skill
copies and global project-skill copies; supported `~/.agents/skills` remains.
Preserve real entries and unrelated targets.

Compare every expected entry with both manifests: require its canonical link
and readable `SKILL.md`, or explicitly report its override. Verify reference
paths, instruction links, no obsolete managed duplicates and unchanged project
status. A second synchronization must make no changes. Required-installation
failures/unresolved conflicts block the stamp; intentional exclusions do not.
Report unchecked runtime discovery as unverified, not live discovery success.
