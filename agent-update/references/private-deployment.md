# Private deployment configuration

Read before bootstrap or planning/writing managed SSH, key, hosts, or cloud-init
files. The private repository owns `deployment.json`; public
`scripts/deployment_config.py` owns its strict format and destination constraints.
Configuration selects values, never authorization to install them.

Under the private synchronization protocol, fetch the registered private origin,
pin the commit, and read `deployment.json` at that same commit as the approved
payload. This configuration has no payload approval record; it supplies values,
while enrollment, approved payloads and the requested operation establish authority.
Validate it with `deployment_config.validate`. Record the source commit
and preserve its JSON as a 0600 snapshot in private task state. Pass that snapshot
as `--deployment-config <path>` to bootstrap, the profile validator, the cluster
key installer, and the managed-file writer. This keeps all stages on one revision.
For a root writer, explicitly stage a root-owned 0600 snapshot before invoking it;
never rely on sudo's HOME or an unregistered root checkout.

Without a snapshot, these tools resolve the existing registration, require an
owned private clean checkout and exact origin match, fetch main, and read its
`deployment.json`. Missing/invalid configuration or failed fetch stops the action;
there is no public default or cached fallback. The default loader does not write
registration or checkout files. Decrypt and approve payloads separately; it does
not replace host binding, digest checks, backups, the writer lock, or postchecks.

The JSON has `schema_version: 1`, `bootstrap` (`dotfiles_url`, `private_url`,
`github_account`), and `paths` (`ssh_include`, `cluster_key`, `cloud_hosts`).
Clone URLs must be literal GitHub URLs: HTTPS for public dotfiles and
`ssh://git@github.com/` for the private source with the dedicated deploy key. Settings are data, never shell source.
The include and key must be direct children of `~/.ssh`; personal SSH names are
reserved regardless of case. The public key uses the configured key path plus `.pub`. The cloud
file must be a dedicated `99-*-preserve-hosts.cfg` under `/etc/cloud/cloud.cfg.d`.
The writer permits only the exact configured destinations plus `/etc/hosts` and
`~/.ssh/config`, with fixed role-specific modes. Root ownership and the sole
`manage_etc_hosts: false` setting remain mandatory for the cloud file. Its cloud
directories must be root-owned, non-writable by others, and not symlinks.

Schema path patterns validate shape, not authorization. The profile validator
also checks every file plan against the exact configured destinations and excludes
key-pair files, whose bytes require the separate key payload approval. Version
2 inventories cannot store SSH file snapshots at any path below `~/.ssh`.
A path-setting change requires an explicit migration plan: preserve existing
keys, includes, routes, and independent local overrides. It never authorizes
renaming or deleting an installed file. Bootstrap reads settings on the trusted
controller before copying keys, so a new server needs no preexisting registration.

## Explicit path migration

A routine refresh does not migrate installed paths. Changed paths or a missing
prior path baseline are a conflict before any key or managed-file write. Resolve
legacy records from the prior pinned configuration and verified installed files;
if that cannot establish ownership and paths, report the missing evidence rather
than treating the host as a new installation.

For an explicitly authorized migration, prepare a plan for the owning host/account
with old and new paths, pinned configuration and payload revisions, exact baselines,
ownership evidence, local key overrides, affected Include directives and routes,
write order, backups, verification and rollback. Preserve independent files and
keys at either destination; a setting change is not replacement authorization.
The caller's approved plan must specify how any retained key override remains
usable at the intended path. Do not silently replace it with the distributed key.

Use the common writer lock and guarded writes with the new protected deployment
snapshot. Create and verify the required new key/include before switching the
managed Include directive in the personal config; check each intermediate state
and the complete candidate's effective options and routes. For cloud paths, use
the separately authorized hosts plan and its root/sole-setting constraints.
Preserve the old files and report their retained paths; removing them requires
explicit scope and proof that no remaining consumer uses them. On failure, use
hash-guarded rollback and leave the success baseline unchanged. Only after all
required checks pass, record the deployment revision and installed paths with the
success evidence. The next routine run must propose no changes.
