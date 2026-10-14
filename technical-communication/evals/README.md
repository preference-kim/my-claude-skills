# Technical communication evaluation

These synthetic cases are maintenance inputs, not runtime instructions. Keep
prompts, traces, judgments, and diagnostic notes outside public repositories in
the local agent-update state directory. Review any published result summary for
its audience; do not publish raw transcripts by default.

## What the pilot tests

Compare three explicitly supplied instruction sets on the same inputs:

- **A:** Baseline scientific/communication principles and applicable writing,
  artifact-content, and audit guidance.
- **B:** A with the modal, terminology, and reply-format conflicts repaired.
  Other structure and content remain. This is a diagnostic variant, not a vendor
  modification or a proposed installation.
- **C:** Candidate principles, technical communication, artifact contracts, and
  audit guidance. Vendor writing passes are absent.

Each case receives one principles excerpt. Operational rules unrelated to the
synthetic task and the separate review-orchestration files are excluded. Some
included source passages still refer to review and publication; the common task
instruction limits the actor to an author draft. This tests author behavior under
that boundary, not execution of the complete artifact workflow.
The six development cases run twice per variant in each available runtime
(36 outputs per runtime). Freeze C before examining the two held-out cases, which
run twice each on C (four more outputs per runtime). Conversation excerpts test
response to supplied feedback, not long-session memory. A versus B probes selected
conflicts; B versus C changes composition and size together and cannot establish
a pure context-length effect.

`build_guidance.py` accepts six checkout paths: baseline and candidate dotfiles,
skills, and audit repositories. Its `--help` lists the arguments. Use inspected,
recorded revisions and an unused output directory; it records hashes and sizes.
The baseline skills checkout needs its pinned vendor sources initialized. The
candidate audit path can be a separate proposal worktree. Do not rebuild a frozen
directory after looking at results.

```bash
python3 technical-communication/evals/run_pilot.py \
  --guidance <frozen-guidance> --output <new-state-directory> \
  --runtime claude --model <configured-model> --effort <configured-effort> \
  --fallback <authorized-fallback-chain> --partition development
```

Run `--partition holdout` into another directory only after C is frozen and the
development campaign's completion and runtime availability have been reviewed.
Do not chain campaigns unconditionally. On an account-wide quota rejection or
reported overage, the runner stops queued work and terminates active process
groups. If termination fails, it reports unverified termination and makes a
bounded reaping attempt; inspect the affected process before any further run.
SIGINT and SIGTERM to the controller also stop queued work and clean up active
groups before the controller exits. Further interrupts are ignored during cleanup.
Exit code 3 requires stopping further model runs under the current account policy. Preserve partial
results. A later authorized rerun uses a new output directory and a recorded reason.
Codex
uses `--runtime codex` without `--fallback`. Keep model/effort fixed within a
runtime; record CLI versions and actual model usage. Do not pool fallback-model
results with the requested model. Existing subscription authentication is used;
Claude child processes discard API-key/static-token overrides without changing
the parent environment or reading credentials.

## Isolation and execution evidence

The runner needs Python 3.9 or later and the selected CLI. It restricts actors to
supplied material. Claude safe mode, disabled skills, and restricted tools exclude
installed customizations; provider-built-in security controls remain enabled.
Inspect initialization records for unexpected skills, plugins, or MCP servers.
Codex actor runs are currently blocked. The prompt inspector can expose ambient
AGENTS or skill instructions, but it does not verify the tool catalog or per-case
tool restrictions under the actor's launch configuration. A clean prompt
inspection therefore cannot authorize a campaign. A verified adapter is required
before Codex evaluation can resume. Do not alter live instructions or copy
credentials to work around this gate.

Document actors receive no tools. The repair actor may edit its synthetic
`converter.py` and run the supplied checker; it cannot modify the checker or
other files. Assess the artifact and observed tool results, not its completion
claim. Hidden checks and `expected`/`critical` fields stay outside the actor's
prompt and workspace. A checker that was invoked but failed is not a pass.

Before scoring, check process completion, delivered context, model identity, and
tool denials. Mark infrastructure failures separately from behavioral findings.
Preserve failed attempts; do not silently replace them with successful reruns.

## Acceptance and review

Freeze the case obligations and rubric before execution. Score task completion,
semantic fidelity, evidence, goal retention, and relevance as 0 (failed), 1
(partial), or 2 (satisfied), with a concrete explanation for a deduction. A critical
failure overrides the aggregate score: lost material meaning, unsupported facts,
unauthorized action, or falsely reported execution/completion.

Give independent reviewers the task, expected obligations, response, and observed
artifact/action evidence under randomized IDs. Withhold variant names, guidance,
and the author's preferences. Evaluate findings against the source; agreement
alone does not establish correctness. Report each case and runtime separately,
including non-improvements and gaps. A candidate needs no critical failure and
coverage of retained requirements; this small pilot cannot prove general
reliability. A revision after a held-out failure needs new held-out cases.

`routing.json` defines three positive document triggers, a short-reply negative,
an adjacent audit collision, and artifact/STE boundaries. Test descriptions as a
catalog separately from supplied-guidance behavior. Specialist workflows are the
entry points; their source links establish dependent loads. A catalog judgment
is not proof of natural discovery in a live client. Separately run the updater's
fixture tests for reference exclusion, managed-link idempotency, overrides, and
advisory notices:

```bash
python3 agent-update/scripts/test_reference_policy.py --scratch <state-directory>
python3 technical-communication/evals/test_runner.py --scratch <state-directory>
```

The runner tests use synthetic child processes and make no model calls.

Only deliberate review may adopt a reference update or activate a candidate.
