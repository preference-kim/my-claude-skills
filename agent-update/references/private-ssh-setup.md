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
   rendering, or that snapshot's include. A nonmatching include already loaded
   by the personal config is a conflict; an unloaded one can be replaced through
   the guarded writer. A personal `Host` stanza is managed only if the candidate
   defines all its names and it appears unchanged in the snapshot. Equal
   effective options alone do not establish ownership.
3. Remove only proven managed copies and their intervening comments/blank lines;
   preserve every other byte. Keep an existing Include in place when it applies
   globally (under `Host *` or before any `Host`/`Match`) and a following
   `Host *` separates personal options. Otherwise replace the incorrectly
   scoped Include with this block at the start; it is the whole candidate when
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
   nothing. Before creating an include, ensure no other Include pattern loads
   its path.
5. Probe affected existing routes, acquire the lock and backup, then write the
   include if changed. Register host keys using `ssh -F` with a protected
   temporary candidate config so the new routes apply; replace the personal
   config last. Each write uses the bytes read during candidate preparation
   (null for an absent file) as its baseline. This prevents concurrent edits,
   not proof of ownership. Verify intermediate states are safe, then complete
   routine post-write checks and hash-guarded recovery if needed.
