# Synchronize SSH configuration

Read [private synchronization](private-sync.md) first. Run on every daily, forced
and requested-edit refresh, including a same-day refresh. Registration and the
approved inventory authorize this stage's first setup, cluster key and
first-contact host trust; the agent performs the checks without a separate
confirmation. Synchronize only the current owner's shared home unless an
explicit fleet request names more targets. Install no hook or scheduler.

Report configuration (`current`, `updated`, `skipped`, `conflict` or `failed`)
and connection results separately. Matching files establish configuration state,
not working access. Name the tested routes, authentication condition and remaining
unverified routes. SSH has its own record and does not hold the public daily
stamp. Missing registration, delegated ownership or an owner without `ssh` is a
configuration skip. An explicit access-repair request remains incomplete until
its requested connection checks pass. Report conflict recovery and continue
independent public refresh work.

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
   `renderer_revision` (public dotfiles commit), `deployment_revision`,
   `ssh_include_path`, `cluster_key_path`, `expected_routes`, `excluded_routes`,
   and `unverified_routes`.
   Keep `route_checks` with each alias's check time, source host/account,
   expected authentication, effective-configuration digest, key fingerprint,
   returned host/account, result and error. Include jump dependencies in the
   digest. Missing records and an empty failure list do not establish success.
   `last-verified-rendering` is the exact installed include;
   `last-verified-config` records the verified personal config and Include
   placement/scope. Conflicting records are a conflict.
3. Load [deployment configuration](private-deployment.md) from the pinned private
   revision. Before installing a key or writing any file, compare the configured
   include/key paths with the last successful paths. For legacy records, recover
   those paths only from that run's pinned deployment or verified config and key
   records; do not infer them from today's settings. A difference or an
   unprovable baseline is a conflict: preserve installed files and success records,
   and use [explicit path migration](private-deployment.md#explicit-path-migration).
   A genuine first setup follows the ownership checks below.
   This stage may write the include selected by `paths.ssh_include`, its Include
   block in `~/.ssh/config`, proven managed copies removed at first setup,
   cluster key, first-contact host keys, and development-server host labels.
   Non-SSH `files` plans and other private keys remain out of scope.
   When rendering references configured `paths.cluster_key`, plan installation
   using the independently approved `cluster-ssh-key` payload (OpenSSH key) and
   `<dotfiles>/scripts/install-cluster-key`. Do not invoke the installer during
   discovery: all drift, ownership and effective-configuration checks must pass
   first. Install under the common writer lock, before the include/config switch;
   the installer guards replacement and derives the public key.
   Preserve a different existing key, record its fingerprint
   as a local override in `last-success.json`, report once and continue.
   For a retained override, compare the accepted key with its recorded
   fingerprint and report `passed-with-override`. Report again if that
   fingerprint changes. This does not pass a task that requires the distributed
   key, whose installation and acceptance remain unverified.
   On development servers, write `~/.config/agent-update/host-labels` (0600):
   `<machine name> <hosts_section> | <name>` per node with `hosts_section`,
   in inventory order. Machine name is `hostname`, falling back to `name`;
   the banner compares the server's short hostname. Personal devices get no
   banner or host-labels file.
4. Check installed drift on every run, even for an unchanged revision:
   - **First setup:** no success record. Read [first setup](private-ssh-setup.md)
     before preparing any candidate, including for an existing include.
   - **Current:** include equals rendering and `render_sha256`. Verify mode,
     active Include and syntax. Apply the connection checks below even when
     the inventory revision is unchanged. After configuration checks pass,
     record its approved revision, digest, renderer/deployment revisions and
     verified include/key paths.
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
connected. Use the same authentication and connection-reuse constraints before
and after. Legacy success records without these conditions are missing evidence.

Use the common writer lock, protected backup, baseline recheck and
`scripts/replace-managed-file.py`; the include is 0600. Installing it may
activate it immediately: verify candidates first and order writes so every
intermediate state is safe. Afterwards verify mode, syntax, effective options,
host trust, affected-route connections and dedicated private-repository access.
Use the connection checks below for affected and requested routes. Unrelated
outages do not authorize network repair or rollout.

A guarded-write failure, bad syntax/mode, effective-option or host-key mismatch,
failed repository access, or a previously connecting route failing after writing
requires reverse-order, hash-guarded rollback. Preserve success records and
record failure separately under the common private protocol. Verify restored
bytes, active Include and syntax after rollback. If a new or previously unreachable route fails only
reachability/access after other checks pass, report configuration `updated` with
the failed connection and record its error in `unverified_routes`. This includes
an identity that no approved payload supplies. Move an entry out of `unverified_routes` only after its required check passes,
an active authorized exclusion is recorded separately, or the approved
source-review delta explicitly retires that route.
A missing rendered stanza does not retire a route. After configuration and
affected-route regression checks pass, advance both verified files and
`last-success.json`, writing hashes last.
Keep failed or missing connection evidence explicit. A second run must propose
no configuration changes.

## Verify route coverage and connections

Derive intended connection aliases and authentication from the approved context
and explicit task targets before inspecting the rendering. Compare that list with
the rendered and effective configuration. A requested alias missing from the
catalog is a coverage defect, even when DNS resolves it. During routine refresh,
report that defect for inventory maintenance. Do not invent a route or drop the
target from the checks. Authentication-only patterns do not add connection targets.
Resolve missing approved routes before deployment. An unapproved removal is a
conflict that preserves installed files. An uncataloged task target needs an
approved route before it can pass or use managed first-contact trust.

For routes that require a local key, verify key selection with `ssh -G <alias>`
without `-i` or authentication overrides. Require the approved readable local key
and the intended account, destination, port, jump chain and host-key policy.
A local private key and public-key file do not establish that the destination
accepts that key. Public-key registration on the destination requires explicit
target authorization and the common backup, lock and concurrent-write checks.

Read the owning profile's optional `ssh_verification` from the approved inventory
before selecting probes. `expected_hostnames` maps a literal route alias to its
allowed returned hostnames; use canonical node hostnames for other routes.
Missing expectations remain unresolved: do not accept a probe's observed hostname
as its own expectation. Establish expectations during explicit inventory
maintenance from inspected endpoint evidence, then publish before using them.
`excluded_routes` maps literal aliases to a `reason` and `resume_condition`.
Keep these aliases in coverage, but do not probe them or traverse them as jumps
while the exclusion applies. Record them separately as `excluded_routes`, never
as passed or as unresolved `unverified_routes`. Keep prior results as dated
history. Source maintenance owns persisted exclusions; a one-run exclusion stays
in that run's record. Reevaluate the resume condition each run; when it is met,
restore the route to probe selection rather than silently marking it verified.
A required route depending on an excluded jump is itself excluded with that
reason. Unexpected failures or missing evidence on other routes remain unverified.

During refresh, probe non-excluded routes with missing evidence, changed effective
settings or key fingerprints, changed hostname expectations, and prior failures.
Always probe non-excluded explicit task targets and affected routes on the
current owner. An explicit maintenance task
can leave unaffected routes untested, but must report that limit.
Reuse unchanged prior evidence only as a dated result, never as a new connection
test. Store digests of normal effective settings and all jump dependencies
separately from probe-only settings, plus the applied hostname expectations.
Compare the same representations on the next run. Record the expected route set
so omissions remain visible when reconciling `route_checks`, `excluded_routes`
and `unverified_routes`.

Run bounded, noninteractive probes from the owning source host and account.
For local-key access, remove `SSH_AUTH_SOCK` and set `IdentityAgent=none` in the
probe child. Disable connection reuse with `ControlMaster=no` and
`ControlPath=none`. Do not supply `-i`, `IdentityFile`, an alternate account or a
replacement route. Keep normal SSH configuration and require
`BatchMode=yes`, `StrictHostKeyChecking=yes`, `ConnectionAttempts=1` and a bounded
`ConnectTimeout`. Apply the same agent and connection-reuse constraints to jump
clients, whose command-line options are not inherited from the destination.
A temporary probe configuration may apply only these constraints and disable
agent forwarding, then include the unchanged normal user and system configuration.
Verify that destination, port, account, key files, jump chain and known-hosts sources
match normal effective settings. Ensure nested jump clients use that same probe
configuration; retain both normal and probe digests. Do not change installed SSH
policy merely to make a probe pass. Check every hop before probing.
If a jump cannot meet the required conditions, report the route as unverified and identify the dependency.
Do not change unrelated authentication policy to force a passing probe.

Require exit status zero and the expected remote host/account from a harmless
command such as `hostname; id -un`. For local-key access, capture the accepted
public-key fingerprint from the same probe's verbose diagnostics and compare it
with the expected local key, including each jump and any recorded override.
Another configured file key
must not mask rejection of the required key. Keep diagnostics in private state.
Follow host-key verification before any probe.
Classify route, trust and authentication failures separately. An agent-assisted
or explicit-key diagnostic can isolate a failure, but cannot pass a local-key
default-access check. Preserve the last successful evidence when recording a
later failure, and report that failure as the current result.

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
