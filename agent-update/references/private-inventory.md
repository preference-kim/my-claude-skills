# Maintain the private inventory

Read [private synchronization](private-sync.md) before registration, source review
or inventory maintenance. These are explicit operations; routine SSH only
consumes the published approved inventory. Keep roles, registrations, names,
source revisions, network scopes, preserved blocks and deployment targets private.

## Register or reconfigure a device

Establish exact hostname, OS account, role and profile from the device and the
user's request. Inspect available keys/routes and ask only for unresolved role
or access choices. Controller capability does not determine device role or hosts
scope. For server setup, follow [bootstrap](private-bootstrap.md). A trusted
personal device obtains the fleet keys there and registers its own profile,
paths and network assumptions rather than copying another device's registration.

All hosts sharing a registration must have the same role; mixed-role devices
need separate registrations and access boundaries. Version-one profiles without
a role require explicit role registration, not an inferred fallback. Write the
reviewed registration atomically as 0600, owned by the account, and validate its
schema. Setup can deploy an approved profile once the fleet keys are present;
otherwise retain a draft and report the missing prerequisite. Hosts-file and
HF/GitHub installation authority remain separate.

Preserve role and node scope independently when editing an owning profile:

- Development servers retain deprecated shared IP aliases at their original
  addresses in the separate legacy block defined by [hosts plans](private-hosts.md).
  A deprecation label does not authorize deletion or a change to personal SSH
  aliases. Preserve approved operational blocks verbatim.
- Personal devices use their approved canonical names/routes. Remove only
  aliases classified as deprecated and authorized for that migration. Preserve
  unrelated entries and the effective destination, port, jump chain, identities
  and host-key policy of retained or renamed routes.
- Delegated profiles retain local configuration; plans belong to the registered
  owner. Non-SSH `files` retain reviewed before/after plans.

## Review and publish source changes

Read source URLs/revisions and conflict-resolution authority from the private
inventory. Inspect current sources and prepare only the requested scope, adding
hosts plans only for an explicit hosts-file request. Classify canonical and
deprecated names from evidence; preserve role, node scope, operational blocks,
routes and key policy. Describe address, naming and policy deltas with their
evidence before approving the plan. Include generated-block marker migrations
and verify retained mappings. Even without a source change, compare local files
with the approved profile.

A configuration-update request authorizes its established scope; unresolved
source conflicts or extra access/route/key changes require clarification. A
source-review-only request produces a candidate, not deployment. Unavailable
sources leave source review unverified, separately from published-profile checks.
Read-only repository holders retain a protected candidate for a maintainer and
report publication pending.

Complete source review before publishing a new inventory. The maintainer
encrypts it to the private recipient list, binds approval to the ciphertext
digest, and publishes the private revision before application. Preserve
independent credential payloads/approvals, registrations and access scope during
an SSH-only update.

## Author shared SSH routes

Use the version-two inventory schema and `scripts/render-private-ssh.py` as the
format contract. Canonical `nodes` own endpoint addresses and reverse ports once.
The shared `ssh` catalog owns `option_sets`, reusable `rules`, ordered network
`contexts` and literal default `bindings`. Profiles select `ssh.context` and only
schema-permitted local identity/known-hosts path bindings. Reuse a matching
network/authentication context; a device name does not justify another one.
Profiles must not contain whole SSH files, copied routes or policy overrides.

The renderer takes verified inventory on stdin and produces include text only;
it does not decrypt, write or connect. It substitutes named `${variables}` once,
preserves OpenSSH `%` tokens, and rejects missing references/variables,
version-two snapshots, scoped option sets and conflicting scalar options.
`IdentityFile`/`CertificateFile` are ordered additive literal paths; the renderer
quotes spaces and comment characters. For
`UserKnownHostsFile`, quote each space-containing path inside the SSH path list.
Catalog identifiers/helper aliases are literal names. Do not store rendered
output back in the inventory or select contexts with shell-startup/`Match exec`
network probes.

Before publishing an SSH edit, read
[effective-configuration checks](private-ssh.md#effective-configuration-checks).
Render every owning SSH profile, require identical output for owners sharing a
home, and verify intended effective routes for every declared connection alias.
Review each changed rule's consumers in all contexts, including unreachable
ones. Record unreachable rollout targets as pending, separately from source
review and offline rendering; local checks do not establish fleet deployment.
