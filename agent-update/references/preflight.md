# Resolve scope and refresh mode

## Repository resolution

Resolve this skill's real path. Use `git rev-parse --show-toplevel` there for the
skills repository, then from its parent for dotfiles. Canonical sources are
`<dotfiles>/AGENTS.md` and `<dotfiles>/skills`. Private-only requests stop public
preflight here and use [private synchronization](private-sync.md).

## Select the public operation

- **Daily:** session-start refresh. If private-state `last-successful-sync`
  contains today's local date, skip public repository/CLI work. Still perform
  cleanup, complete manifest/link verification and approved SSH fetch/drift checks.
- **Forced:** `/agent-update`, `$agent-update` or an explicit refresh runs all
  stages regardless of date.
- **Requested edit:** use the review-only path below for an isolated proposal.
  Otherwise run the full refresh, including SSH, then apply the request before
  validation/publication.
- **Link repair:** perform configured link checks even if today's refresh passed.
- **Private-only:** explicit server-configuration or enrolled-credential work
  runs only requested targets/payloads under the private protocol. It does not
  run public CLI updates, cleanup, installation or upstream reconciliation and
  leaves the daily stamp unchanged, unless refresh was also requested.

Generic refresh authorizes neither source review/bootstrap nor hosts-file or
HF/GitHub writes. Private state is
`${XDG_STATE_HOME:-$HOME/.local/state}/agent-update`.

## Review-only instruction proposals

When the user requests a PR or isolated proposal without live activation, record
clean source revisions and use separate branches/worktrees. Do not run the live
refresh, private synchronization, installation, CLI updates, or success stamping
as a prerequisite. Validate candidate manifests and migrations in fixtures.
The user-requested proposal workflow owns publication and review. Preserve live
entry points while preparing and reviewing the proposal.

Ordinary full refreshes pull the `main` branches used by the live installation
and follow the updated instructions. Publication, merge, and activation are
separate authorizations. Complete required validation and obtain merge approval
before merging; publishing a proposal branch does not authorize its merge.
When activation is withheld, keep the proposal unmerged unless the already-installed
refresh path honors a persisted hold before any pull or submodule update. Verify
the reader, its state location, and an explicit-approval release condition from a
fresh session using the retained installation. A local note or a rule available
only in the incoming revision does not establish that protection. If the reader
is absent or unverified, report the missing prerequisite; changing live policy
requires separate authorization.

With that protection verified, preserve live checkout revisions and entry points
after an authorized merge. Record the installed and merged revisions and pending
activation decision in the hold's documented state location. Do not run a
post-merge refresh, live submodule update, installation, or success stamping until
activation is approved and the hold is explicitly released.

## Validate the host layout

Read gitignored `<dotfiles>/agent-file-sync.local.yaml`. Require `mode` to be
`host-global` or `moreh-dev`; absence/invalidity blocks installation, not an
invitation to infer a mode. Change this host-local file only on request; use
`agent-file-sync.example.yaml` as its template.

For `moreh-dev`, require nonempty `moreh_dev_root`. Resolve absolute paths as
written and relative paths from dotfiles; canonicalize and require an existing
directory whose `git rev-parse --show-toplevel` is that exact directory. Do not
expand shell expressions or find/create/clone a substitute. A bad project root
blocks project synchronization and the success stamp; continue independent
user-scope installation when mode is valid.

## Lock and update

Use private-state `lock` as an atomic directory, recording hostname/PID. Remove
it on exit; reclaim only when its recorded process is dead on that same host.

Before tracked changes, inspect both repositories' `git status --short --branch`.
Require `main`, no unrelated tracked/untracked work and fast-forward relations
to `origin/main`. Fetch origins, pull dotfiles with `--ff-only`, synchronize
submodule URLs and initialize/update recursively, then switch skills to `main`
and pull `--ff-only`. Otherwise stop without stash, rebase, reset or force-push.
Read [upstream decisions](upstream.md) before upstream comparison.

If pulled instructions changed, re-read AGENTS/this skill and use later
references from the updated checkout. Updated guidance governs the remaining
stages; its change alone does not require clarification.

Before editing an existing user-owned nested skill, verify ownership, clean
state and fast-forward relation to its own `origin/main`; switch to `main` and
fast-forward through that origin. Keep unrelated/vendor nested repositories at
their recorded commits. [Publication](publication.md) requires the changed child
to publish before either parent.
