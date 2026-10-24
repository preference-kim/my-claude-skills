# First SSH setup

Read [private synchronization](private-sync.md) and
[SSH synchronization](private-ssh.md) before this path. It applies whenever no
SSH success record exists, including partial
deployments or absent `~/.ssh/config` and `~/.ssh`. Finish with the routine
stage's verification and records.

1. Read this profile's config/include plans from its last approved version-one
   inventory revision, with the same approval-digest checks. Without that
   snapshot, no inline stanza is a proven managed copy.
2. An include is managed if it equals the current rendering, an earlier approved
   rendering, or that snapshot's include. Preserve any existing nonmatching
   include as a conflict, whether loaded or not, until the user explicitly
   authorizes replacement or a migration preserving it. Until resolved, write
   neither the include nor the personal config. An absent include can
   be created through the guarded writer with a null baseline. A personal
   `Host` stanza is managed only if the candidate defines all its names and it
   appears unchanged in the snapshot. Equal
   effective options alone do not establish ownership.
3. Remove only proven managed copies, including comments/blank lines within
   those copies; preserve every other byte. Keep an existing Include directive
   for the configured managed path in place when it applies
   globally (under `Host *` or before any `Host`/`Match`) and a following
   `Host *` separates personal options. Otherwise replace the incorrectly
   scoped directive for that managed path with this block at the start; it is the
   whole candidate when
   config is absent:

   ```
   Host *
   Include <paths.ssh_include>
   Host *
   ```

   Substitute the exact validated `paths.ssh_include` from
   [deployment configuration](private-deployment.md); never write the placeholder.

4. Apply the routine effective-configuration checks. A hidden, defeated or
   dropped personal rule is a conflict: identify its resolution and write
   nothing. Require the complete candidate to load the managed path exactly
   once, in global scope. Normalize only proven managed directives; an
   overlapping personal Include pattern is a conflict.
5. Probe affected existing routes, acquire the lock and backup, then install
   and verify any required key before writing the include if changed. Register
   host keys using `ssh -F` with a protected temporary candidate config so the
   new routes apply. `-F` suppresses the system config: explicitly reproduce its
   evaluation, including global scope and relative Include resolution, in the
   protected evaluation copies. Before comparing a changed candidate, verify that
   the unchanged copy's `ssh -G` options equal normal evaluation for each affected
   alias; a mismatch blocks writing. Replace the personal config last and verify
   its normal effective options against the accepted candidate. Each write uses the bytes read during candidate preparation
   (null for an absent file) as its baseline. This prevents concurrent edits,
   not proof of ownership. Verify intermediate states are safe, then complete
   routine post-write checks and hash-guarded recovery if needed.
