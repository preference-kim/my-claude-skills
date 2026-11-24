# Apply hosts-file plans

Read [private synchronization](private-sync.md) first. On every refresh, including
same-day runs, apply the approved `/etc/hosts` plan when the validator returns
`apply_hosts_on_refresh: true` for this physical personal owner and account.
An explicit hosts request can also select this stage. The standing scope covers
only `/etc/hosts`. Cloud-init changes and [source or profile edits](private-inventory.md)
each need explicit scope. Inspect the physical host independently of its home mount.

## Accept the plan

The approved `hosts_scope.managed_node_names` selects exact canonical IDs from
`nodes`; role or labels do not select scope. `hosts_scope.blocks` assigns each
selected node once, with approved titles and node order. Render matching
`# BEGIN <title>` / `# END <title>` markers and requested cluster subsections;
omit empty blocks. `preserved_hosts_blocks` are literal text, kept byte-for-byte.
Check their names/IPs against selected nodes. An incompatible IP requires a
reviewed block revision, not a duplicate definition. Keep local OS/site entries
and localhost outside generated blocks.

Canonical and deprecated aliases must be disjoint and unambiguous across nodes
and files. A development server uses `deprecated_alias_policy: separate-block`:
retain existing deprecated aliases at their original addresses between
`# BEGIN Legacy aliases - will be deprecated` and
`# END Legacy aliases - will be deprecated`. A personal device uses `omit`:
remove only reviewed deprecated aliases listed in `authorized_alias_removals`.
Neither reorganization nor a deprecation label changes personal SSH routes or
schedules deletion.

Non-SSH `files` plans are restricted to `/etc/hosts` and an explicitly planned
`paths.cloud_hosts` from [deployment configuration](private-deployment.md).
The profile validator checks binding/layout before application. For each reviewed `before` and `after`:
current `after` requires verification only; current `before` permits replacement.
A different current file permits a three-way merge only for verified disjoint
hunks that pass the SSH equivalence checks below. Overlap, unknown ownership or
unapproved routing/key differences is a conflict. Preserve local overrides,
include structure, identity files, host-key policy and retained routes; a rename
cannot silently replace a jump route with direct access or change its key.

## Apply and verify

Use the common writer lock, exact backup, baseline recheck and guarded replacer.
First compare bytes, root ownership, mode and name resolution. If current,
record verification without requesting elevation. A required write needs local
administrator authorization. Use existing noninteractive sudo if available.
On an opted-in personal device with an interactive user, use its local sudo or
native administrator prompt for the reviewed write, with the pinned root-owned
deployment snapshot. Never collect a password in chat or grant standing sudo.
If unavailable or declined, save the protected candidate, mark hosts pending,
and continue independent SSH work. Record the physical owner, inventory revision,
content digest and result after verification.

If a boot manager regenerates hosts, inspect its effective configuration and
datasource overrides. An approved cloud-init plan may install
`manage_etc_hosts: false` in the dedicated drop-in as root, mode 0644. A missing
drop-in uses a null baseline; back up an existing one. Verify the merged value
without initialization modules or reboot, and report configuration verification
separately from a reboot test.

Before applying or probing, read the
[SSH effective-configuration and host-key checks](private-ssh.md#effective-configuration-checks).
Compare every retained literal alias's effective route and key/host-key options
with `ssh -G`, including wildcard/include precedence; verify `ssh_equivalence`
pairs for added names and all replacement routes. Record authorized removals
separately. Verify candidate addresses and unique managed names. After writing,
check content, owner, mode, retained alias/`HostName` resolution, and
representative noninteractive SSH connections. Preserve the current connection
through checks. On failure use the common hash-guarded rollback. If SSH
configuration also changed within its authorized scope, reverify private
repository access with its dedicated settings.
