# Plan Review Criteria

Apply only criteria relevant to the proposed work and its repository or operating environment. Do not impose language, framework, commit-count, or style rules that are unrelated to the plan.

## Decision criteria

### Goal and evidence

- Is the objective concrete, and are success and failure distinguishable?
- Are observed facts, assumptions, hypotheses, inferences, and open questions separated?
- Can material claims be checked against identified sources or measurements?

### Scope and ownership

- Are in-scope and out-of-scope changes explicit and coherent?
- Are affected interfaces, state, data, users, and systems identified?
- Are dependencies, permissions, responsible owners, and coordination points present?
- Does the plan preserve applicable repository and user instructions?

### Mechanism and execution

- Does each step explain how it advances the objective rather than merely naming activity?
- Are ordering constraints, prerequisites, invariants, and state transitions clear?
- Does the plan address the root cause or justify why a narrower treatment is sufficient?

### Risk and recovery

- Are relevant failure modes, edge cases, resource limits, and stop conditions covered?
- Are destructive or externally visible actions authorized at the point they occur?
- Is rollback, cleanup, or another safe recovery path defined where failure could leave material state behind?

### Evaluation and acceptance

- Do comparisons use an appropriate baseline or control when the conclusion depends on one?
- Are metrics capable of distinguishing the claimed outcome from plausible alternatives?
- Are validation procedures reproducible, with required inputs, environment, and conditions stated?
- Are acceptance criteria concrete enough to decide whether implementation may finish or proceed?

## Verdicts

- `Approve`: The plan is executable and its remaining uncertainties are explicitly bounded by adequate checks or stop conditions.
- `Revise`: The objective remains sound, but material omissions or unsupported decisions must be corrected before execution.
- `Reject`: The plan's objective, premise, authorization, or approach is unsupported or unsafe enough that local edits cannot make it executable without a new decision.

Do not lower the verdict merely for optional improvements. Tie every required change to a concrete consequence, unresolved premise, or failed criterion.
