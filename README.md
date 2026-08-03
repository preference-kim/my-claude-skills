# Shared Agent Skills

Canonical shared skills used by Codex and Claude. This repository is mounted as
the `skills` submodule of `preference-kim/dotfiles`; tool-specific skill
directories contain links to these canonical directories rather than copies.

## Skills

| Skill | Description |
|-------|-------------|
| [agent-update](agent-update/) | Synchronizes shared agent guidance across hosts while preserving local policy. |
| [gh-review-own-pr](gh-review-own-pr/) | Submits the current branch and coordinates approval-gated PR reviews. |
| [humanizer](humanizer/) | Rewrites AI-sounding text. Submodule tracking [blader/humanizer](https://github.com/blader/humanizer). |
| [plan-review](plan-review/) | Reviews implementation plans for scope and risk before coding starts. |
| [skill-maker](skill-maker/) | Authors and refines SKILL.md files; audits drafts against an anti-patterns checklist. |
| [write-technical-pr](write-technical-pr/) | Drafts and audits technical pull-request descriptions as current-design documents. |

## Storage policy

- Keep one canonical top-level directory per skill, with `SKILL.md` at its root.
- Track locally maintained or adapted skills directly in this repository.
- Use a nested submodule only for a verbatim third-party skill whose independent
  provenance and update boundary should remain visible. `humanizer` is the
  current example.
- Do not clone this repository into `~/.codex/skills` or `~/.claude/skills`.
  The `agent-update` skill maintains per-skill links in both real directories,
  preserving unrelated host-local skills.

## Setup

Clone `preference-kim/dotfiles` with recursive submodules, then invoke
`agent-update`. It validates the canonical manifest and installs every shared
skill for both tools.

## References

- [Designing, Refining, and Maintaining Agent Skills at Perplexity](https://research.perplexity.ai/articles/designing-refining-and-maintaining-agent-skills-at-perplexity) — principles for authoring and maintaining agent skills ("a Skill is a folder, not a file").
