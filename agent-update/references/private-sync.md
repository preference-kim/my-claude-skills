## Synchronize this host

Run this protocol only when the user explicitly requests synchronization or
repair of server configuration or enrolled credentials. Explicit credential setup
also permits that credential workflow; enrollment and approval remain required.
Daily refreshes, generic `agent-update` requests, link repair and instruction edits
do not activate it: skip private
repository fetches, decryption and payload application. A previous enrollment or
approved inventory revision is not a standing request to synchronize. Skipping
this unrequested stage does not block public refresh success.

For an explicit request, use its target and payload scope, then check
`~/.config/agent-update/private-sync.json`. If absent, report that private sync is
not enrolled; do not infer targets or borrow credentials. Fetch again regardless
of the daily refresh stamp. Running this skill on one host updates that host; a
fleet run requires explicit target scope and reports each target separately.
Reviewing inventory sources alone does not authorize deployment.

On an enrolled host, a draft, pending, conflicting or failed requested payload
blocks synchronization success. If synchronization was requested together with
an agent refresh, it also blocks a complete refresh stamp; independent public
maintenance may continue. Unrequested payloads are skipped without blocking it.

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
commit and digest separately for `inventory`, `hf-token` and enrolled `github-token`. Missing, draft or
mismatched approval blocks that payload; other payloads may proceed independently.
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

## Install an enrolled GitHub account credential

GitHub account access is optional and requires explicit user authorization; read-only
repository enrollment alone does not authorize it. Registration must supply both
`github_identity` and `github_account`. When GitHub credential synchronization is
requested, successful application or verification of this enrolled payload is
required for synchronization success. Keep `github-token.age`, its recipient list
and approval separate from inventory and HF. A credential group may reuse its HF age identity for
this payload only when the same members are explicitly authorized for GitHub access;
reuse couples future decryption access, not token rotation or approvals. Any membership
change involving that identity requires authorization for both credentials, or separate
identities before access is granted. Every host mounting the credential home must be in
the approved scope. Preserve independent inventory and HF identities.

Use the same pinned-revision, approval-digest and rollback checks above. Clear
`GH_TOKEN`, `GITHUB_TOKEN` and enterprise-token overrides only in installer and
verification children; never print their values. Inspect `gh auth login --help` before
installation; consult official documentation if installed behavior differs. Validate the
candidate's account with `gh api --hostname github.com user` with only the candidate
token injected into its child environment before changing stored auth. Require a
case-insensitive match to `github_account`; never store a token in arguments or Git
URLs. Candidate failure means no credential write. Inspect existing accounts first;
preserve their entries and report an unexpected active account unless the user has
authorized switching it.

Under the shared-home writer lock, back up the resolved standard gh configuration and
affected Git configuration, including modes, outside public Git with 0700 backup
directories and 0600 files. Reject unknown symlinks and concurrent changes. Compare the
current stored token in memory to avoid rewriting unchanged auth. Pipe the decrypted
token to `gh auth login --hostname github.com --git-protocol https --with-token`.
Enrollment of a headless server authorizes `--insecure-storage` when no secure
credential store is configured. Enforce 0700 on its config directory and 0600 on
`hosts.yml`; this stores the usable token locally in plaintext. Never silently downgrade
an existing secure store. An existing account entry with no local token can indicate a
keyring on another shared-home host; investigate instead of overwriting it. Do not
replace unrelated host/account entries or change AI CLI credentials.

`gh auth setup-git --hostname github.com` configures GitHub.com HTTPS credentials for
the whole user account, including existing repositories. Back up and report replaced
GitHub helpers. Run it and verify without token overrides that `gh api --hostname
github.com user` matches the registered account. Verify a required private Git
repository through HTTPS with `GIT_TERMINAL_PROMPT=0`. Use a private inventory
verification target, or an HTTPS rendering of the registered private repository URL for
this read-only probe without changing its origin. Configure approved GitHub repositories
to use HTTPS when needed; preserve existing SSH routes and keys, and the private sync
checkout's independent read-only bootstrap authentication. Enrolled servers must retain
an SSH origin with their explicit deploy-key command; reject an HTTPS bootstrap origin
rather than letting the global account helper capture it. Do not claim that HTTPS
credential helpers authenticate arbitrary SSH remotes. Account access is limited by the
token's scopes, organization authorization and the user's rights. For user-owned
harness repositories with read-only SSH fetch keys, configure an HTTPS
`remote.origin.pushurl` and check repository push permission through `gh`. The push URL
survives submodule URL synchronization. Preserve vendor origins and the private bootstrap
checkout's read-only policy. Do not test write access by creating external objects.

Record per-host account, private-repository read verification and payload revision
without token values or hashes. Authentication failure blocks credential success; retain
recovery backups and report partial results. After a post-write failure, restore only if
current files still match this run's recorded writes; otherwise report the conflict for
recovery. Report token-scope rejection as a payload error. Never log out or revoke a
shared token to repair one host. Rotation requires updating the approved private
payload, then verifying authorized members before revoking the previous credential.

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
registration. A group shares one read-only repository key and separate inventory and HF age
identities. The optional GitHub payload follows the explicit reuse rule above. Generate group keys on
the maintainer and distribute them only over authenticated SSH to approved
members authorized for each payload. Group membership alone does not grant HF
access. Never commit private keys to either repository or copy personal SSH keys. Account credentials require explicit enrollment
authorization for that payload and target scope. Keep group
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
an already recovered account token. Discuss rotation and any published-history rewrite
before performing them. Keep recovery identities backed up only at a destination
approved by the user; losing all identities loses access to their payload.
