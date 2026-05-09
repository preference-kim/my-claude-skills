---
name:
description:
---

# Skill Name

## When Loaded

State the domain-specific objective in one or two sentences. Do not restate the description.

## Gotchas

- Add failure modes the base agent would plausibly miss.
- Prefer negative examples and boundary cases over general advice.

## Workflow

1. Start with the smallest action that changes task quality.
2. Keep steps outcome-oriented, not command recipes.
3. Stop when additional guidance would only restate ordinary agent behavior.

## Conditional Files

Read bundled files only when their condition applies:

- `references/...`: heavy conditional context.
- `scripts/...`: deterministic logic the agent should run or adapt.
- `assets/...`: templates or output resources the agent should fill.
