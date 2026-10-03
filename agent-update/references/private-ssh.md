# Shared SSH configuration

Use one private source for destinations and routes. A profile selects a network
context and may bind existing local identity or known-hosts paths; it must not
contain SSH file contents, individual route copies, or host-specific policy
overrides. Host registration and shared-home ownership remain separate from this
selection. Keep credentials in their existing stores.

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
not currently reachable. Render every owning SSH profile before publication.
Require identical output for owners sharing a home. The same destination's
address or reverse port must be defined once; contexts choose how to reach it.
Do not copy rendered output back into the inventory. Preserve unrelated hosts,
credential payloads, registration and access scope during an SSH-only change.

## Migration and deployment

Keep the existing private-sync approval, revision, lock, backup, baseline and
rollback checks. Derive concrete before/after file plans from the approved
catalog and the current local files; store those plans only in private local
state. Version-one SSH snapshots are migration inputs, never a second source
after conversion. Before planning an existing generated file, compare it with the
last verified rendering recorded in local state. Use the approved version-one
snapshot for first migration; unknown provenance or differing content is a local
change to review, not a new baseline to silently accept. Record the resulting
rendering and digest after successful deployment. Preserve exact recovery copies
outside Git.

Keep personal rules in `~/.ssh/config` and include the generated file at a
reviewed stanza boundary, with `Host *` scope before and after it. Preserve the
location of an existing include. During first migration, remove only the exact
managed stanzas whose ownership and replacement have been reviewed. Leave
unrelated bytes and local overrides intact; report an overlapping override as a
conflict instead of silently defeating it with include precedence. Never perform
automatic network probes from shell startup or `Match exec` to choose a context.

Compare old and candidate effective configurations with the same OpenSSH client,
account, system configuration and include dependencies. Inspect existing `Match
exec` commands before running `ssh -G`: configuration evaluation may execute them.
Check every retained literal alias, helper gateway, new alias, and representative
local wildcard match. Compare repeated options as ordered lists, including all
identity and certificate files. Permit only explicitly reviewed differences,
recorded with their old and new values. An identical hostname alone does not
establish route or authentication equivalence.

Installing an included file can activate it immediately. Review the intermediate
state of each write, keep the current connection open, and verify the candidate
before writing. The guarded replacer permits first creation of the generated
include with a null baseline; it rejects concurrent creation. Verify mode 0600,
effective configuration, existing host-key trust, representative noninteractive
connections and private-repository access afterwards. A second run must propose
no changes. Record unreachable consumers as pending, separately from source and
offline-rendering validation; do not claim a fleet rollout from local checks.
