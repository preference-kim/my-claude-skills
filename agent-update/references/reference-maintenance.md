# Pinned writing references

`reference` in `.installation-policy.json` means an approved source retained for
deliberate consultation, with no Codex or Claude discovery link. `humanizer` and
`simple-english` stay at reviewed gitlink revisions. Ordinary writing uses
`technical-communication`; an explicit request or skill-maintenance question can
justify reading selected reference material. Do not load both sources by default.

## Advisory update check

During a full daily or forced `agent-update`, run:

```bash
python3 <skills>/agent-update/scripts/reference_updates.py --skills-root <skills>
```

The command reads the registry, committed gitlink pins, and GitHub metadata with
`gh api`. It does not fetch, checkout, change a pin, or install a source. A source's
declared branch is used when present; otherwise its upstream default branch is
queried. State lives under the existing agent-update state directory; tests can
pass `--state-dir` explicitly.

Report a short advisory when at least five upstream commits have accumulated
since the reviewed pin or last notified revision. A successful notice advances
only that source's local notification cursor. Changing its pin, remote, or branch
resets the cursor to the new reviewed baseline. Do not repeat an unchanged notice.
Report non-forward history once until it recovers or the source is reviewed.
Lookup failures retain the last successful cursor and produce one advisory per
outage; they do not block unrelated refresh work. A registry/state failure also
leaves pins unchanged and is reported as an unavailable check.

## Deliberate adoption

A notice is not authorization to incorporate changes. For a separately requested
review, inspect the old and proposed revisions, identify relevant changes, and
test their effect on our skill before proposing an update. Preserve intentional
divergence and review publication scope. Updating a reference pin does not restore
discovery, execute upstream instructions, or change the routine writing workflow.
