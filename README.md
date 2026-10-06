# Shared Agent Skills

Canonical shared skills used by Codex and Claude. This repository is mounted as
the `skills` submodule of `preference-kim/dotfiles`; tool-specific skill
directories contain links to these canonical directories rather than copies.

## Skills

| Skill | Description |
|-------|-------------|
| [agent-handoff](agent-handoff/) | Prepares a reviewed task handoff and the opening prompt for a fresh session. |
| [agent-update](agent-update/) | Synchronizes shared agent guidance across hosts while preserving local policy. |
| [gh-review-other-pr](gh-review-other-pr/) | Reviews another author’s PR and prepares a pending review. |
| [gh-stack](gh-stack/) | Manages dependent branches and pull requests. |
| [gh-review-own-pr](gh-review-own-pr/) | Submits the current branch and coordinates approval-gated PR reviews. |
| [humanizer](humanizer/) | Rewrites AI-sounding text. Submodule tracking [blader/humanizer](https://github.com/blader/humanizer). |
| [simple-english](simple-english/skills/simple-english/) | Drafts English PR descriptions, handoffs, and technical documentation. Unmodified upstream skill from [AminBlg/SimpleEnglish](https://github.com/AminBlg/SimpleEnglish). |
| [skill-maker](skill-maker/) | Authors and refines SKILL.md files; audits drafts against an anti-patterns checklist. |
| [stop-bullshit](stop-bullshit/) | Checks unsupported claims and evasive reasoning; independently maintained at [preference-kim/stop-bullshit](https://github.com/preference-kim/stop-bullshit). |
| [tt-device-investigation](tt-device-investigation/) | Investigates TT device anomalies; installed only in the configured Moreh checkout. |
| [write-technical-pr](write-technical-pr/) | Drafts technical PR descriptions and finalizes them after independent prose and evidence review. |

## Storage policy

- Keep one canonical top-level directory per approved skill. A vendor submodule
  can declare its nested skill directory with `skill-path` in `.gitmodules`;
  other skills keep `SKILL.md` at their root.
- `.publication-policy.json` lists exact public paths. Review content and audience
  before adding a path. Install only tracked skills and approved submodules;
  ignored local directories must not enter the shared skill manifest.
- Keep private operational resources and internal evidence outside this worktree.
  See [publication policy](https://github.com/preference-kim/dotfiles/blob/main/PUBLICATION.md).
- Track locally maintained or adapted skills directly unless they have a separate
  authoritative repository. Use a nested submodule for that repository's update
  boundary: `stop-bullshit` is user-owned; `humanizer` and `simple-english`
  retain their upstream files unchanged.
- `.installation-policy.json` assigns every approved skill to `user` or
  `moreh-dev`. User skills install in both modes at `~/.agents/skills` (Codex)
  and `~/.claude/skills` (Claude); project skills install only in `moreh-dev`,
  at the checkout’s `.agents/skills` and `.claude/skills`.
- Keep discovery roots as real directories with per-skill canonical symlinks.
  Do not clone this repository into them. Preserve unrelated local skills.
  Resolve each skill’s canonical directory before reading relative resources,
  including sibling `review-common` and dotfiles `agent-guidance`.

## Setup

Clone `preference-kim/dotfiles` with recursive submodules, then invoke
`agent-update`. It validates publication approval and complete scope classification, then
installs the expected skills for both tools. Invalid project configuration does
not block user skills, but prevents a successful refresh stamp.

## References

- [Designing, Refining, and Maintaining Agent Skills at Perplexity](https://research.perplexity.ai/articles/designing-refining-and-maintaining-agent-skills-at-perplexity) — principles for authoring and maintaining agent skills ("a Skill is a folder, not a file").
