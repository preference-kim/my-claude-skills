# Shared Agent Skills

Canonical shared skills used by Codex and Claude. This repository is mounted as
the `skills` submodule of `preference-kim/dotfiles`; tool-specific skill
directories contain links to these canonical directories rather than copies.

## Skills

| Skill | Description |
|-------|-------------|
| [agent-update](agent-update/) | Synchronizes shared agent guidance across hosts while preserving local policy. |
| [gh-review-other-pr](gh-review-other-pr/) | Reviews another author’s PR and prepares a pending review. |
| [gh-stack](gh-stack/) | Manages dependent branches and pull requests. |
| [gh-review-own-pr](gh-review-own-pr/) | Submits the current branch and coordinates approval-gated PR reviews. |
| [humanizer](humanizer/) | Rewrites AI-sounding text. Submodule tracking [blader/humanizer](https://github.com/blader/humanizer). |
| [skill-maker](skill-maker/) | Authors and refines SKILL.md files; audits drafts against an anti-patterns checklist. |
| [stop-bullshit](stop-bullshit/) | Checks unsupported claims and evasive reasoning; independently maintained at [preference-kim/stop-bullshit](https://github.com/preference-kim/stop-bullshit). |
| [write-technical-pr](write-technical-pr/) | Drafts and audits technical pull-request descriptions as current-design documents. |

## Storage policy

- Keep one canonical top-level directory per approved skill, with `SKILL.md` at its root.
- `.publication-policy.json` lists exact public paths. Review content and audience
  before adding a path. Install only tracked skills and approved submodules;
  ignored local directories must not enter the shared skill manifest.
- Keep private operational resources and internal evidence outside this worktree.
  See [publication policy](https://github.com/preference-kim/dotfiles/blob/main/PUBLICATION.md).
- Track locally maintained or adapted skills directly unless they have a separate
  authoritative repository. Use a nested submodule for that repository's update
  boundary: `stop-bullshit` is user-owned; `humanizer` is a verbatim third-party skill.
- Do not clone this repository into `~/.codex/skills` or `~/.claude/skills`.
  The `agent-update` skill maintains per-skill links in both real directories,
  preserving unrelated host-local skills.

## Setup

Clone `preference-kim/dotfiles` with recursive submodules, then invoke
`agent-update`. It validates the canonical manifest and installs every shared
skill for both tools.

## References

- [Designing, Refining, and Maintaining Agent Skills at Perplexity](https://research.perplexity.ai/articles/designing-refining-and-maintaining-agent-skills-at-perplexity) — principles for authoring and maintaining agent skills ("a Skill is a folder, not a file").
