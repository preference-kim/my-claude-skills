# Skill Anti-Patterns

Use this checklist during CREATE and REFINE critique. The core reference is Perplexity's "Designing, Refining, and Maintaining Agent Skills at Perplexity"; these rules adapt that methodology for Claude Code skills. The goal is not to make a skill look like documentation; the goal is to make another agent load the right context at the right time and then perform better than it would without the skill.

Run these checks in order. A routing failure invalidates later prose polish because the body may never load.

## 1. Unevaluated Routing

The description is a routing interface. Treat every new skill and every description change as behavior that needs positive, negative, and adjacent examples.

Detect this when a draft:

- has no routing eval pack
- changes a description without comparing old and new routing behavior
- adds broad terms like "documents," "research," "coding," or "review" without negative examples
- cannot name the adjacent skill or workflow it must not steal

Before:

```yaml
description: Use when the user asks for review, writing, documentation, or coding help.
```

After:

```yaml
description: Use when the user asks to draft, critique, refine, or improve a Claude Code SKILL.md or bundled skill folder.
```

Before accepting a description, write or reuse a routing eval pack with at least three positives, one negative, and one adjacent collision case. If the revised description cannot pass those examples, keep iterating before writing.

## 2. Description As Documentation

The description is the routing layer. It is paid for in every session and read before the skill body is available. A weak description explains what the skill contains; a strong description describes when the user wants it loaded.

Detect this when the description:

- starts with "This skill provides" or summarizes the body
- omits the user verbs that should trigger it
- is broad enough to steal unrelated requests from neighboring skills
- cannot explain why a negative utterance should not route here

Before:

```yaml
description: This skill explains our deployment workflow and includes release checklist details, commands, and rollback notes.
```

After:

```yaml
description: Use when the user asks to prepare, verify, ship, or roll back a service release using this repository's deployment process.
```

Changing a description after a skill exists is risky. Check it against positive, negative, and adjacent utterances before accepting the change.

## 3. Non-Load-Bearing Content

Every paragraph should pass the failure-without-this test: would the agent likely get the task wrong without it? If not, cut it or move it out of the loaded body.

Detect this when content:

- explains basic concepts instead of operational gotchas
- repeats the same rule in multiple sections
- includes motivational framing
- preserves planning notes that do not affect execution
- teaches a common tool at beginner level

Before:

```markdown
Skills are useful because they package repeatable instructions and help agents perform specialized tasks more consistently.
```

After:

```markdown
Ask for positive and negative routing utterances before drafting; otherwise the description usually becomes too broad.
```

The second sentence changes behavior. The first only explains the category.

## 4. Missing Gotcha Capture

Skills should become append-mostly where failures accumulate as durable negative examples. A critique that finds a reusable failure mode should not disappear into the chat transcript.

Detect this when a refinement:

- fixes a mistake without naming the failure mode
- discovers an adjacent routing collision but does not record it
- repeats a previous correction that could have been a gotcha
- treats gotchas as optional prose instead of primary content
- turns one incident into a general rule but keeps incident-specific IDs,
  timestamps, or examples in always-loaded skill text even though they are
  not load-bearing

Before:

```markdown
I tightened the description so it does not trigger on PR reviews.
```

After:

```markdown
Candidate gotcha: Do not add "review" to the description for skill-making; it collides with code review and plan-review routing. Keep "review" as a post-load synonym only.
```

At the end of critique, list candidate gotchas separately. Ask whether each belongs in the target skill's gotchas or in this anti-pattern file.

Single-incident anchoring: when turning one incident into a reusable rule,
generalize the failure mode and avoid embedding incident-specific IDs/examples
in always-loaded skill text unless they are load-bearing.

## 5. System-Prompt Recap

A skill should not restate behavior the agent already receives globally. Recapping general coding, safety, editing, formatting, or collaboration rules wastes context and can conflict with newer system instructions.

Detect this when a paragraph says things like:

- read files before editing
- preserve user changes
- use concise communication
- do not run destructive commands
- prefer existing project conventions

Those may be good rules, but they belong in global instructions, not a conditional skill, unless the skill has a domain-specific exception or sharper local interpretation.

Before:

```markdown
Always inspect the repository before making changes. Use the existing style and avoid unnecessary refactors.
```

After:

```markdown
When refining a skill, inspect its frontmatter and any referenced bundled files before judging whether the body is load-bearing.
```

The revised version is specific to skill critique; the original is generic agent behavior.

## 6. Misused Hierarchy

A skill is a folder, but extra files should earn their keep. Use `references/` for heavy conditional knowledge, `scripts/` for deterministic logic the agent would otherwise rewrite, and `assets/` for reusable output resources. Do not create folders just to look complete.

Detect underuse when a `SKILL.md` grows into long conditional sections, pasted schemas, or many examples that only apply sometimes. Detect overuse when the skill creates empty folders, redundant README files, or reference files that contain the same rules as the body.

Before:

```markdown
## API Errors
[300 lines of status codes and retry behavior inline]
```

After:

```markdown
If the API returns a non-2xx response, read `references/api-errors.md` before retrying or reporting failure.
```

The body should tell the agent when to load the spoke. The spoke can hold the bulky detail.

## 7. Volatile Inline References

Skills should not embed facts that change faster than the skill is maintained. This includes active API shapes, model lists, pricing, UI labels, current policies, and external service behavior. Either require live lookup, point to a reference file with clear ownership, or avoid the detail.

Detect this when a skill hard-codes:

- latest model names or version-specific recommendations
- current endpoint behavior for a third-party service
- pricing, limits, quotas, or rapidly changing rules
- long copied excerpts from web documentation

Before:

```markdown
Use model `example-2026-04-01` because it is currently the best model for summaries.
```

After:

```markdown
For model choice, check the official provider docs at task time and choose the current summarization-capable model.
```

Durable local policy can stay inline. Volatile public facts should be looked up or isolated so drift is easier to spot.

## 8. Deterministic Command Recipes

Do not turn a skill into a brittle list of commands the model already knows how to adapt. Exact commands are useful when the command itself is the reusable artifact, when flags are easy to get wrong, or when a local script exists. Otherwise, describe intent and constraints.

Detect this when the skill lists ordinary shell or git steps in sequence:

- `git status`, then `git add`, then `git commit`
- `mkdir`, then `touch`, then `cat`
- a fixed read/edit/test sequence with no domain-specific reason

Before:

```markdown
Run `git status`, create a branch, edit SKILL.md, run `git diff`, and then summarize the changes.
```

After:

```markdown
Revise the target skill in place only after confirmation. Preserve unrelated worktree changes and summarize the final diff.
```

Keep exact commands when they encode real local knowledge, such as a repo-specific validation script or a fragile conversion command.

## Source

Adapted from Perplexity Research, "Designing, Refining, and Maintaining Agent Skills at Perplexity": https://research.perplexity.ai/articles/designing-refining-and-maintaining-agent-skills-at-perplexity
