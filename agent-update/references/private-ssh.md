# Synchronize SSH configuration

Read [private synchronization](private-sync.md) first. Run on every daily, forced
and requested-edit refresh, including a same-day refresh. Registration and the
approved inventory authorize this stage's first setup, cluster key and
first-contact host trust; the agent performs the checks without a separate
confirmation. Synchronize only the current owner's shared home unless an
explicit fleet request names more targets. Install no hook or scheduler.

Report one result: `current`, `updated`, `skipped`, `conflict` or `failed`;
include conflict recovery and continue the public refresh. SSH has its own
success record and does not hold the public daily stamp. Missing registration,
delegated ownership or an owner without `ssh` is a reported skip.

## Render and select the path

1. Complete common enrollment, schema/profile validation, per-run private fetch,
   pinned revision/descent, approval and decryption checks. Render with
   `<dotfiles>/scripts/render-private-ssh.py --profile <owner>` and verified
   inventory on stdin. A failure leaves installed files and records unchanged;
   it does not establish that they are current. This stage consumes the published
   inventory; [inventory maintenance](private-inventory.md) is a separate explicit
   action.
2. Keep owner-local state in `<private-state>/private-ssh/<profile>/` (0700/0600).
   `last-success.json` records `profile`, `inventory_revision`,
   `inventory_sha256` (ciphertext), `render_sha256`, `config_sha256`,
   `renderer_revision` (public dotfiles commit), and `unverified_routes`.
   `last-verified-rendering` is the exact installed include;
   `last-verified-config` records the verified personal config and Include
   placement/scope. Conflicting records are a conflict.
3. This stage may write the generated `~/.ssh/moreh_cluster.conf`, its Include
   block in `~/.ssh/config`, proven managed copies removed at first setup,
   cluster key, first-contact host keys, and development-server host labels.
   Non-SSH `files` plans and other private keys remain out of scope.
   When rendering references `~/.ssh/moreh_cluster_sunho`, pipe its independently
   approved `cluster-ssh-key` payload (OpenSSH key) into
   `<dotfiles>/scripts/install-cluster-key`; it guards installation and derives
   the public key. Preserve a different existing key, record its fingerprint
   as a local override in `last-success.json`, report once and continue.
   On development servers, write `~/.config/agent-update/host-labels` (0600):
   `<machine name> <hosts_section> | <name>` per node with `hosts_section`,
   in inventory order. Machine name is `hostname`, falling back to `name`;
   the banner compares the server's short hostname. Personal devices get no
   banner or host-labels file.
4. Check installed drift on every run, even for an unchanged revision:
   - **First setup:** no success record. Read [first setup](private-ssh-setup.md)
     before preparing any candidate, including for an existing include.
   - **Current:** include equals rendering and `render_sha256`. Verify mode,
     active Include and syntax; record the revision and retry
     `unverified_routes`, with no other cluster probes.
   - **Update:** include equals `last-verified-rendering` but the new rendering
     differs. Follow the update checks below.
   - **Conflict:** include differs from its verified baseline, or the Include
     was moved/removed. Preserve files.
   On Current and Update paths, compare changed personal config with
   `last-verified-config`. Record edits that leave managed names unchanged.
   A new/changed personal rule assigning a conflicting value to a managed name
   is a conflict even if the Include hides it.

## Accept and verify a change

For Update or First setup, apply the effective-configuration checks below.
The approved delta authorizes managed changes; unrelated personal rules remain.
An overlapping personal rule is a conflict. Missing dependencies or unsupported
client options fail the stage before writing. New/changed routes and jump
helpers must carry an explicit IP or resolvable DNS `HostName`, without a hosts
write. Probe each affected existing route before writing to establish whether it
connected.

Use the common writer lock, protected backup, baseline recheck and
`scripts/replace-managed-file.py`; the include is 0600. Installing it may
activate it immediately: verify candidates first and order writes so every
intermediate state is safe. Afterwards verify mode, syntax, effective options,
host trust, affected-route connections and dedicated private-repository access.
Use bounded noninteractive probes only for affected routes; unrelated outages
do not authorize network repair or rollout.

A guarded-write failure, bad syntax/mode, effective-option or host-key mismatch,
failed repository access, or a previously connecting route failing after writing
requires reverse-order, hash-guarded rollback. Preserve success records and
record failure separately. If a new or previously unreachable route fails only
reachability/access after other checks pass, report `updated` and record its
error in `unverified_routes` (including an identity no approved payload supplies).
Retry host-key registration and connection on later refreshes; remove an entry
when it passes or leaves the rendering. After verification, advance both verified
files and `last-success.json`, writing hashes last. A second run must propose
no changes.

## Effective-configuration checks

Before `ssh -G`, inspect existing `Match exec`: evaluation can execute commands.
Use the same client, account, system config and include dependencies for old and
candidate configurations. Compare retained literal aliases, helper gateways, new
aliases and representative local wildcard matches. Repeated identity/certificate
options are ordered lists.

A new name takes candidate values. An existing name may change only where the
removed proven managed copy or previous include supplied the old value and the
candidate include supplies the new one; record both. Other differences defeat
or drop personal rules. Also evaluate personal rules alone, without the Include,
against empty config: any different value they set for a managed name is a
conflict, including hidden rules for new names. An identical hostname alone
does not prove route/authentication equivalence.

Determine affected routes from complete effective before/after options; shared
authentication changes can affect existing routes. Approved connection aliases
require destination and jump resolution/probes. Authentication-only `Host`
patterns require option comparison, not invented destinations or DNS/hosts
repair. A declared route missing `HostName` remains a required route. Resolve
catalog/source disagreements through explicit maintenance rather than
reclassifying a failing alias. Version-one snapshots are first-setup evidence,
not a second source after conversion.

## Host-key verification

Before probes, check trust for the approved destination, port and jump route
under hostname, address, `HostKeyAlias` and prior names. Reuse existing trust;
renaming does not make a known server a first contact. A saved or approved key
mismatch stops that route; preserve the saved key and report it.

For a managed server without trust, compare any approved fingerprint before
recording. If none exists, the stage authorizes recording the first presented
key, without separate confirmation. Use `StrictHostKeyChecking=accept-new` only
for that initial connection. Register jumps individually in route order before
the destination; keep every existing known-hosts source active. This establishes
first-contact trust, not independent server identity. Never use `no`/`off`,
discard trust records, or change the private repository's pinned host keys.

Record host keys under the common lock/backup protocol, preserving unrelated
entries and saving destination/fingerprint in private state. Verify afterward
with `StrictHostKeyChecking=yes` and retain the configured host-key policy.
