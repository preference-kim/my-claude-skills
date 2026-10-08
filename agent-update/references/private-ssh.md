# Shared SSH configuration

Use one private source for destinations and routes. A profile selects a network
context and may bind existing local identity or known-hosts paths; it must not
contain SSH file contents, individual route copies, or host-specific policy
overrides. Host registration and shared-home ownership remain separate from this
selection. Keep credentials in their existing stores.

## Routine agent refresh

Run this stage on every daily, forced and requested-edit agent refresh, even
when the public daily stamp is current. This skill directs the agent to run the
existing renderer and guarded writer; it installs no background scheduler or
shell hook. Synchronize only the current configuration owner's shared home.
An explicit fleet request may name additional owners; ordinary refreshes do not
SSH into other hosts to update them.

Registration and the approved inventory authorize every write in this stage,
including first setup, the cluster key and first-contact host keys. The agent performs the checks
in this document itself: "reviewed" means checked against these criteria, never
a request for user confirmation. End the stage with one outcome: `current`,
`updated`, `skipped`, `conflict` or `failed`. Report it in one line, say how a
conflict can be resolved, and continue the refresh without waiting for an answer.
The stage has its own success record and runs on every refresh, so its outcome
does not hold the public daily stamp.

1. Follow `private-sync.md` for exact host/account registration, ownership,
   repository authentication, clean checkout, pinned revision, approval digest
   and decryption. Missing registration, a delegated profile or an owner without
   `ssh` is a reported skip. Do not bootstrap a host, copy keys from another host or
   synchronize HF/GitHub credentials during this stage.
2. Use `${XDG_STATE_HOME:-$HOME/.local/state}/agent-update/private-ssh/<profile>/`
   for owner-local state (directory 0700, files 0600). `last-success.json` records
   `profile`, `inventory_revision`, `inventory_sha256` (ciphertext digest),
   `render_sha256`, `config_sha256`, `renderer_revision` (the public dotfiles
   commit) and any `unverified_routes`. `last-verified-rendering` contains the
   exact installed include; `last-verified-config` records the verified personal
   entry point and Include placement/scope.
3. Fetch the published private revision regardless of the public daily stamp.
   When a success record exists, require the revision to descend from its
   recorded revision. Render the selected owner with
   `scripts/render-private-ssh.py --profile <owner>`, passing the verified
   decrypted inventory on stdin. If fetch, descent, approval, decryption or
   rendering fails, end the stage as `failed` with files and records unchanged;
   the installed files are not thereby current. Never apply the profile's non-SSH
   `files` plans or change `/etc/hosts`, cloud-init or private keys other than the
   cluster key below. In
   `~/.ssh/config`, change only the Include block and the managed copies that
   first setup removes. Register server host keys under
   [Host-key verification](#host-key-verification). When the rendering references
   `~/.ssh/moreh_cluster_sunho`, pipe the decrypted `cluster-ssh-key` payload (the
   OpenSSH private key) into `<dotfiles>/scripts/install-cluster-key`, which installs
   it with the guarded writer and derives the public key. A different existing key is
   kept: record its fingerprint as a local override in `last-success.json`, report it
   once, and continue the stage. On a `development-server`, also write
   `~/.config/agent-update/host-labels` (0600) for the shell banner: one
   `<machine name> <hosts_section> | <name>` line for each inventory node that has
   a `hosts_section`, in inventory order. The machine name is the node's `hostname`, or its `name` when
   the node has no `hostname`. The banner compares it with the server's short
   hostname. A personal device shows no banner and gets no host-labels file.
4. Choose the path from the installed state, checking drift on every run even
   when the private revision has not changed. If the records disagree with each
   other, report a conflict.
   - No success record: follow [First setup](#first-setup), whether or not an
     include already exists.
   - Current: the installed include equals the rendering and `render_sha256`.
     Verify mode, the active Include and SSH syntax, record the revision and retry
     any `unverified_routes`. Make no other cluster connection probes.
   - Update: the installed include equals `last-verified-rendering` and the
     rendering differs. Continue with step 5.
   - Conflict: the installed include differs from `last-verified-rendering`, or
     the Include was moved or removed after setup. Preserve the files.

   On the Current and Update paths, inspect the diff when `~/.ssh/config` differs
   from `last-verified-config`. Advance the record for edits that leave managed
   names unchanged. An added or changed personal rule that sets a different value
   for a managed name is a conflict even though the Include hides it.
5. On the Update and First setup paths, compare the candidate under
   [Effective-configuration checks](#effective-configuration-checks). The
   approved published delta authorizes the change. Preserve unrelated personal
   rules. End the stage as `conflict` for an overlapping personal rule, or as
   `failed` for an unresolved dependency or unsupported client option, with the
   files preserved. Identify connection routes from the approved catalog and
   source review, using the distinction below. New or changed routes must carry
   an explicit IP or resolvable DNS `HostName` for the destination and its jump
   helpers; do not depend on a hosts-file write. Before writing, probe each
   affected existing route once so step 7 can tell a regression from an
   unreachable route.
6. Under the shared-home writer lock, save the prior files and metadata in a
   unique protected backup and recheck each baseline. Use
   `scripts/replace-managed-file.py` for each write; the generated include has
   mode 0600. Afterwards verify mode, SSH syntax, effective options, host-key
   trust, affected-route connection probes and private-repository access. Probe
   only affected routes, with bounded noninteractive timeouts. Do not let an
   unrelated offline cluster trigger network repair or a fleet rollout.
7. A guarded-write failure, invalid syntax or mode, an effective-option mismatch,
   a host-key mismatch, failed private-repository access, or an existing route
   that connected before the write and fails after it is a failed update. Roll
   back in reverse write order, restoring each file only if it still matches this
   run's write; otherwise report the concurrent edit. Keep the success records
   unchanged and record the failure separately. A new route, or one that did not
   connect before the write, does not fail the update when its probe fails only
   for reachability or access after every other check passes. Report `updated`,
   record the route and its error (such as an identity file that no approved
   payload provides) in `unverified_routes`, and retry its host-key
   registration and probe on later refreshes. Drop it from the list when a retry
   passes or the rendering no longer defines it. Advance `last-verified-rendering`,
   `last-verified-config` and `last-success.json` only after verification,
   writing the hash record last.

Source-document and chat review belong to explicit configuration maintenance.
This refresh consumes the reviewed private repository; it does not revise or
publish its inventory.

## First setup

A host without a success record may hold its managed routes inline in
`~/.ssh/config`, may already have an include from its version-one snapshot, an
earlier deployment or an interrupted write, or may have neither, even without
`~/.ssh/config` or `~/.ssh`. First setup brings any of these states to the current
rendering in the same refresh, then writes the records.

1. Read the snapshot: this profile's `~/.ssh/config` and
   `~/.ssh/moreh_cluster.conf` plans in the last approved version-one inventory
   revision of the private repository, under the same approval-digest checks.
   A host without one has no proven managed copies.
2. An existing include is managed when it equals the current rendering, the
   rendering of an earlier approved revision, or the snapshot's include plan; it
   is the previous include for the checks below. An include that matches none
   of these is a conflict when `~/.ssh/config` loads it; otherwise step 6
   replaces it.
3. A personal `Host` stanza is a managed copy when the candidate defines all of
   its names and the stanza appears unchanged in the snapshot. Equal effective
   options alone do not prove ownership; keep every other stanza.
4. Build the candidate `~/.ssh/config`: remove the managed copies and the comment
   or blank lines that sit only between them, and keep every other byte. An
   existing Include of the include path is correctly scoped when it applies to
   every host (under `Host *` or before any `Host` or `Match` line) and a
   `Host *` line separates it from following personal options. Keep such an
   Include in place. Otherwise put this block at the start of the file, replacing
   an incorrectly scoped Include; without `~/.ssh/config`, the block alone is the
   candidate. The first `Host *` gives the Include global scope; the second
   returns the following personal rules to their own scope.

   ```
   Host *
   Include ~/.ssh/moreh_cluster.conf
   Host *
   ```

5. Apply the effective-configuration checks. If a personal rule would be
   defeated, dropped or hidden, report a conflict that names it and the
   resolution (edit or remove the rule, or change the inventory through explicit
   maintenance), and write nothing.
6. Install through routine steps 5 to 7 in this order: probe affected existing
   routes, take the lock and backup, write the include if it differs from the
   rendering, register host keys with `ssh -F` and a protected temporary copy of
   the candidate `~/.ssh/config` so registration follows the new routes, then
   replace `~/.ssh/config` if it changed. Before creating a new include, make
   sure that no Include pattern other than the one kept or placed in step 4
   already loads its path; if one does, report a conflict and write nothing. For
   each write, pass the target's bytes as read when the candidate was prepared
   (none for an absent file) as the expected prior content; this guards against
   concurrent edits and does not prove ownership. The writer creates a missing
   `~/.ssh` with mode 0700.

## Source and rendering

Inventory version 2 keeps addresses and endpoint metadata on canonical `nodes`.
Its `ssh` catalog contains shared `option_sets`, reusable `rules`, and network
`contexts`, with shared literal defaults in `bindings`. Rules select node names
or literal helper aliases. Contexts list
rules in explicit order and supply their network defaults. Profiles select one
context through `ssh.context` and may supply only the local path bindings allowed
by the schema. Reuse an existing context when its network and authentication
requirements match; a device name alone does not justify a new context.

Read the schema and run `scripts/render-private-ssh.py --profile <owner>` with
the verified decrypted inventory on stdin. The renderer outputs
`~/.ssh/moreh_cluster.conf` content; it does not decrypt, write, connect, or deploy.
It substitutes named `${variables}` once and leaves OpenSSH `%` tokens intact.
Missing references and variables, SSH snapshots in version 2, scope directives in
option sets, and conflicting scalar options within a rule are errors. Ordered
`IdentityFile` and `CertificateFile` entries remain additive. Their values are
literal paths and the renderer quotes spaces and comment characters. A
`UserKnownHostsFile` value is an SSH path list; quote any individual path containing
spaces in that list. Catalog identifiers and helper aliases must be literal names.

Review an edited shared rule for every consuming context, including consumers
not currently reachable. Render every owning SSH profile before publication and
verify that every declared connection alias has its intended effective route.
Require identical output for owners sharing a home. The same destination's
address or reverse port must be defined once; contexts choose how to reach it.
Do not copy rendered output back into the inventory. Preserve unrelated hosts,
credential payloads, registration and access scope during an SSH-only change.

A `Host` pattern can select authentication policy without defining a connection
route. A rule containing only key, agent or host-key options does not promise
that every matched physical hostname resolves. Determine the intended connection
aliases from the approved route rules and reviewed source, not from every emitted
`Host` token. A declared alias remains a required route if its `HostName` was
accidentally omitted; do not reclassify it to bypass a failed check.

Compare effective authentication options for all affected names. Apply destination
resolution and connection probes to declared routes and their jump dependencies.
Determine affected routes from their complete effective configuration before and
after the update; a shared authentication change can affect an existing route.
An unresolved name matched only by authentication policy does not block deployment
of valid routes. Do not invent a route or change DNS or hosts files for that name.
If the catalog and source disagree about a name's role, report the conflict.

## Host-key verification

Apply this check before connection probes during SSH setup or synchronization.
Use the approved destination, port and jump route. Check existing trust under
its hostname, address and `HostKeyAlias`, including prior names when renaming a
route. Reuse that trust; a new alias does not make a known server a first contact.
If a saved key or approved fingerprint differs from the server's key, stop the
affected route and report the mismatch. Do not remove or replace the saved key
to make the connection succeed.

For a managed server with no existing trust, compare the presented key with any
approved key or fingerprint before recording it. If neither is available, the
SSH stage includes trusting and recording the key presented on first contact;
no separate confirmation is required. Use
`StrictHostKeyChecking=accept-new` only for that initial connection. Register
new jump hosts individually, in route order, before the destination. Keep all
existing known-hosts sources active. This trusts the first connection; it
does not independently prove the server's identity. Never use `no` or `off`,
discard known-hosts records, or change the private repository's pinned host keys.

Use the shared-home writer lock and backup policy when recording host keys.
Preserve unrelated entries and record the destination and key fingerprint in
private state. After registration, verify the connection with
`StrictHostKeyChecking=yes` and retain the configured host-key policy.

## Effective-configuration checks

Keep the existing private-sync approval, revision, lock, backup, baseline and
rollback checks. Store before/after plans only in private local state and keep
exact recovery copies outside Git. Version-one SSH snapshots are first-setup
inputs, never a second source after conversion. Never perform automatic network
probes from shell startup or `Match exec` to choose a context.

Compare old and candidate effective configurations with the same OpenSSH client,
account, system configuration and include dependencies. Inspect existing `Match
exec` commands before running `ssh -G`: configuration evaluation may execute them.
Check every retained literal alias, helper gateway, new alias, and representative
local wildcard match. Compare repeated options as ordered lists, including all
identity and certificate files. A name that did not exist before takes the
candidate's values. For an existing name, permit a difference only when a
managed copy this write removes or the previous include supplied the old value
and the candidate include supplies the new one; record both values. Any other
difference defeats or drops a personal rule. Because the Include comes first, a
personal rule can also be hidden without any difference showing. Evaluate the
personal rules alone (the candidate configuration without its Include block)
against an empty configuration: any option they set for a managed name, new or
existing, to a value different from the candidate is a conflict. An identical
hostname alone does not establish route or authentication equivalence.

Installing an included file can activate it immediately. Order writes so each
intermediate state is safe, keep the current connection open, and verify the
candidate before writing. The guarded replacer permits first creation of the
generated include with a null baseline; it rejects concurrent creation. A second
run must propose no changes. During explicit fleet maintenance, record
unreachable consumers as pending, separately from source and offline-rendering
validation; do not claim a fleet rollout from local checks.
