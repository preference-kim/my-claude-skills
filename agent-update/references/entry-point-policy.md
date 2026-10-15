# Entry-point policy

Read this when changing shared layout policy. The host chooses
`agent-file-sync.local.yaml` from the tracked example; its gitignored `mode`
and `moreh_dev_root` never transfer to another host.

[Preflight](preflight.md) owns mode/root validation and daily, forced, edit and
private-only cadence. [Installation](installation.md) owns canonical manifests,
scope, exact links, conflicts and migration. Preserve their separation:

- Instruction location is host-global or one explicitly configured development
  checkout.
- Skill scope comes independently from `.installation-policy.json`: user skills
  are installed for both runtimes in both modes; project skills stay in that
  checkout; pinned references receive no discovery links.
- Publication scope is separate from installation. Local project links do not
  authorize project contributions.

Before changing any of those contracts, read their owning references and
[upstream decisions](upstream.md); preserve intentional differences through
semantic reconciliation rather than wholesale replacement.
