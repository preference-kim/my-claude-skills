# PR finding contract

## Team review policy

Before reviewing code or validating existing feedback, the orchestrator resolves
`checkout` and `repository_url` literally from `~/.config/agent-update/private-sync.json`. Require an exact origin URL match. With existing repository
authentication, fetch `origin/main`, record its commit, and read `review-policy.md` using `git show <commit>:review-policy.md`. Do not alter the private
checkout's files, branch, or remote. A failed fetch cannot be replaced by cached
references. Missing or invalid registration, an origin mismatch, missing
document, or failed source access means team policy coverage is unavailable;
report that limit without treating it as evidence that no policy applies.

The private document owns repository matching, policy sources, and author scope.
Apply matching policies alongside the reviewed repository's review instructions,
within each rule's stated scope. Record the private configuration revision in
private task state and each applied policy's source revision for the review
report. Report not applicable only after reading the configuration and
establishing that no entry matches. Keep team identifiers, source locations, and
policy contents out of public skill files.

Give isolated reviewers the resolved coverage state: applied, not applicable, or
unavailable, with a brief reason for the latter two. For applied policies,
supply the policy and its source revision, including contents when source access
is unavailable to the leaf. Leaves use this supplied context without reading
private registration or unrelated configuration; an absent coverage state or
missing applicable policy is a limitation to report to the orchestrator. The
policy supplies review criteria; it does not change the owning workflow's
permissions or delegation rules.

## Findings and isolated context

Establish the problem, why it occurs, and what outcome this PR promises. Use the
description, base behavior, and relevant callers, issues, or design history to
understand the constraints. For staged work, identify the contribution promised
here. Qualify conclusions that depend on an unverified cause or unclear scope.

### Identify defects

- Give a minimal trigger, the required behavior, what the code does, and the
  consequence. For input validation or construction, show which valid input is
  rejected or fails to build, or which invalid input is accepted. Compare with
  the base before calling a gap in new support a regression. Consider concurrency,
  security, compatibility, and resource lifetime where they affect the contract.
- For a changed interface, trace what each material value means, who owns it,
  and how callers use it. Distinguish protocol requirements from representation
  choices. Explain the concrete effect of any ownership or contract ambiguity.
- Distinguish test collection, fixture setup, a wrong expected value or
  comparison, and a missing case or assertion. Say what the test verifies and
  which faulty behavior can pass. If both implementation and test need changes,
  identify the fix and the check that catches it.

### Propose improvements

1. **Would merging this PR resolve the underlying problem?** Trace the original
   case to the outcome the caller would observe after merge. If the concern
   survives, show where and why. Explain which different approach would address
   the cause and what observation would establish success.
2. **How well does each material implementation choice serve its intent?** Even
   when the code works, compare it with a feasible alternative under the same
   constraints. For efficiency, identify the workload and the extra work or
   measured cost. Distinguish a count of operations from a measured change in
   latency or throughput. Request a measurement when it could change the decision.
   For structure, compare the responsible layer, abstraction, or established pattern.
   Name a concrete benefit for a caller or maintainer and the trade-off it brings.

### Report actionable findings

Keep one concrete, high-confidence finding per comment at the smallest relevant
changed location. Explain its consequence, the proposed action, and what the
cited sources establish. Say whether the PR needs the change before merge or
it is a suggestion, and why. Omit speculative or style-only preferences. A review
may have no findings. Preserve required prefixes and material uncertainty. Use
connected prose and only the detail each finding needs.

Prefer the smallest coherent change at the layer that owns the behavior. For a
test request, give the input and expected result that distinguish the alternatives.
Use component helpers or direct inputs, and widen to integration only if a local
test cannot observe the failure. When a short repository pattern fits, adapt it
as a code suggestion and cite the example.

### Isolated reviewers

Before preparing isolated leaf prompts, read
[stop-bullshit](../stop-bullshit/SKILL.md). Supply this contract, the applicable
reasoning and communication principles from canonical AGENTS.md, and that skill's
loaded instructions. Provide contents if canonical files are inaccessible.
Leaves apply the check directly, without another critic or orchestration skill.
Check both the reviewed material and comments before any permitted write.
The orchestrator also applies this contract and the final substance check when
consolidating all reviewers' findings and after the last prose edit.
