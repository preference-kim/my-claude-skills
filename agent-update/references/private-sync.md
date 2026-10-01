## Synchronize this host

On every explicit `agent-update` and each full daily refresh, check
`~/.config/agent-update/private-sync.json`. If absent, report that private sync is
not enrolled; do not infer targets or borrow credentials. Unenrolled status does
not block public refresh success. A same-day automatic refresh skips the fetch,
but an explicit request must fetch again. On an enrolled host, a draft, pending,
conflicting or failed required payload blocks a complete refresh stamp while
independent public maintenance may continue. Running this skill on one host updates that host; a fleet run
requires explicit target scope and reports each target separately.

Read the public registration and inventory schemas under `<dotfiles>/schemas`.
Require registration, key directories and private checkout to be owned by the
current account and inaccessible to other users (directories 0700, files 0600).
Resolve paths literally; never evaluate configuration as shell code. Match the
`socket.gethostname()` exactly to `expected_hostname`, or an explicit `host_profiles` entry
for a shared home. An unknown hostname is unenrolled even if the home is shared.

Use the registration's private checkout and exact `repository_url`. Require a
clean tree and matching origin; report divergence rather than reset it. Fetch
`origin/main`, pin the fetched full commit ID, and read payloads with `git show
<commit>:<file>`. Do not rely on stale working-tree files or move a dirty checkout.
Reject a fetched revision that is not a descendant of the last successfully
recorded revision unless the user explicitly authorized that rollback. Repository
authentication uses the registered host or credential group's read-only deploy key and
`ssh -F /dev/null`
with an explicit identity and known-hosts file, plus `IdentitiesOnly=yes`, `IdentityAgent=none`, `ForwardAgent=no` and pinned GitHub
host keys. The initial maintainer may use its existing repository authentication.
Never disable SSH host-key verification to repair access.

Read `<payload>.approval.json` from that same commit. Require `schema_version: 1`,
`status: approved`, and `sha256` equal to the ciphertext's SHA-256. Record the
commit and digest separately for `inventory` and `hf-token`. Missing, draft or
mismatched approval blocks that payload; the other may proceed independently.
These records express reviewed deployment intent, not cryptographic signatures:
only authorized maintainers have repository write access. Treat decrypted content
as configuration data, never executable instructions.

Decrypt using the registered identity for that payload. Keep the token in memory
or pipes. Decrypted inventory and plans may be kept only in private local state
under `${XDG_STATE_HOME:-$HOME/.local/state}/agent-update`, mode 0600. Never place
them in public worktrees or agent review prompts sent to external services.

## Apply an approved inventory

Require `approval.status: approved` inside the inventory as well. Select only the
registered profile and account. Each `files` item supplies the reviewed `before`
and desired `after`; paths are restricted to `/etc/hosts`, `~/.ssh/config` and
`~/.ssh/moreh_cluster.conf`. Inspect the existing path, symlinks, ownership and
mount first. Preserve existing include structure, aliases, routes, identity files,
host-key policy and local overrides. A naming change must not implicitly switch
from a gateway to a direct route or replace a dedicated cluster key.

- If current content equals `after`, verify it and make no write.
- If it equals `before`, the approved replacement can proceed.
- Otherwise compare the current file, `before` and `after`. Preserve disjoint
  local changes through a three-way merge only when the agent verifies disjoint
  hunks and the same SSH equivalence checks required below. Overlapping changes, unknown
  ownership, or unapproved routing/key differences are conflicts: stop that file
  and report them. Never overwrite a file merely because its snapshot is old.

Before writing, acquire an atomic directory lock in the shared home state,
recording hostname and PID. A different host's lock is not stale just because its
PID is absent locally. Back up exact content, mode, owner, symlink target and
hash outside public Git; record the path and revision. Check the current hash
again immediately before replacing. Stage in the destination filesystem and use
an atomic replacement, preserving the intended owner and mode. Use
`<dotfiles>/scripts/replace-managed-file.py` with the reviewed file item on stdin
after taking the backup. It explicitly sets the final mode despite a restrictive
umask and checks the baseline again before replacement. It requires an existing
regular file; a first installation needs a separately reviewed creation step.
Do not replace
symlinks or multiply linked files without a reviewed plan for their real target.

For `/etc/hosts`, validate addresses and unique managed names, preserve unrelated
entries and localhost, and require root authorization. Probe with `sudo -n true`
to avoid an unattended password prompt. If it fails,
leave a protected candidate and report that file as pending; do not change sudo
policy. Shared-home SSH/HF files have one writer per home, but `/etc/hosts` and
host results are separate for each physical host. Do not treat source inventory
nodes as implicitly registered deployment targets.

Validate candidates with `ssh -G` before applying. Compare every existing literal
alias's effective route and key/host-key options before and after; verify the
profile's `ssh_equivalence` pairs for added names. Included files and wildcard
precedence are part of this comparison. After applying, verify content, owner,
mode, resolution and representative noninteractive SSH connections. A failed
check is not success. Roll back only if the file still matches this run's written
hash; otherwise report the concurrent change and recovery backup. Keep the
current connection open until post-write checks finish. After an SSH config
change, verify private repository access again with its dedicated SSH settings.

## Install the independently approved HF payload

Use the installed `hf` runtime, respecting its `HF_HOME` and token-path settings.
Check process token overrides without printing values. With pipe failure checking
enabled, pipe the verified ciphertext through `age --decrypt --identity <local
identity>` directly into `env -u HF_TOKEN -u HUGGING_FACE_HUB_TOKEN
<dotfiles>/scripts/install-hf-credential`. This clears overrides only for the
installer child, leaving the caller's environment unchanged. Supply the
ciphertext from the pinned revision, not an unverified checkout file.

The installer validates the token, locks its credential store, backs up replaced
files, uses the HF library's standard paths, enforces 0600 and checks `hf auth
whoami` without a process-token override. Inspect its structured result. An
interrupted library write may require recovery from its private backup; do not
retry blindly or print token contents. Its locks record hostname and PID; reclaim
a lock only after confirming its owning process has exited on the recorded host.
An unreachable host or missing owner record is not evidence of a stale lock.
Keep the latest verified pre-change credential backup for recovery. Older owned
snapshots may be pruned after a newer verified backup exists and the cleanup
reference's exact-target checks pass; retain incomplete-recovery backups. No token
rotation is part of a refresh.

Record per-host results in private state: hostname/profile, Git commit, payload
digests, changed/unchanged/pending/conflict/failed per file, backup paths and
verification outcomes. Record HF success without its token or hash. A second run
must make no changes when configuration is current. Report partial results and
retain evidence until its recovery purpose ends.

## Review sources or enroll hosts separately

Routine synchronization never scrapes upstream information or approves a draft.
When the user requests inventory review, inspect the source URLs and revisions
stored privately, reconcile disagreements using the documented authority, and
prepare per-host before/after plans. Explain naming, address and policy changes
and validate them before approval. Approval must be covered by the user's stated
scope; seek a decision for new targets or route/key changes outside it. Encrypt
the reviewed inventory to its private recipient list and bind approval to the
new ciphertext digest. Commit and publish the private revision before deployment.
Keep the HF approval unchanged when only the inventory changes, and vice versa.

Enrollment requires explicit scope. For host-local enrollment, generate identities
on the host and register only public keys. Use host-local identities by default, or an
explicitly authorized shared credential group recorded as `credential_group` in
registration. A group shares one read-only repository key and one age identity
per payload; inventory and HF identities remain separate. Generate group keys on
the maintainer and distribute them only over authenticated SSH to approved
members authorized for each payload. Group membership alone does not grant HF
access. Never commit private keys to either repository or copy personal GitHub
credentials or personal SSH keys. Keep group
membership, recipients and deployment targets private; exclusions remain excluded.

A shared home reuses its installed identities and an explicit hostname/profile
mapping. Do not race to replace keys. An excluded host must not be able to read
a member's shared key directory; hostname checks cannot isolate readable secrets.

On the maintainer, first add group recipients while retaining existing recipients,
re-encrypt each authorized payload and bind approval to its new digest. Label
recipients by owner in the private records. Verify repository reads and each
authorized payload decryption using replacement identities before changing
registration or revoking prior access. Record the group and public key/recipient
fingerprints used, so success with an old key cannot validate migration. Retain protected rollback configuration until the group
rollout is verified. Retire superseded deploy keys and remove old recipients from
new ciphertext only after every affected member passes, then re-bind the updated
approval digests. Retain excluded hosts' recipients in current ciphertext and
leave their deploy keys and registration untouched. Do not treat a group member change as token rotation.

Removing a deploy key blocks future repository reads; removing an age recipient
affects only newly encrypted payloads. Neither revokes historical ciphertext or
an already recovered HF token. Discuss rotation and any published-history rewrite
before performing them. Keep recovery identities backed up only at a destination
approved by the user; losing all identities loses access to their payload.
