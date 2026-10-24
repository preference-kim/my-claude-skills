# Bootstrap and fleet keys

Read [private synchronization](private-sync.md) before explicitly requested
device bootstrap or fleet-key lifecycle work. These operations are separate from
routine refresh and credential installation.

## Fleet keys

Development servers and trusted personal devices use the same
`~/.config/agent-update/fleet/` (0700): `fleet.agekey`,
`private-repo-ed25519`, its `.pub`, and pinned `github_known_hosts` (files 0600).
The fleet age identity decrypts every payload; the deploy key reads the private
repository. Encrypt each payload to the single fleet recipient. Private
`access/keys.json` records purposes, fingerprints/recipient, master location and
installed paths. Never commit unencrypted keys. A registration naming older
identities requires reporting undecryptable payloads and bootstrap from a trusted
host.

The master directory is in the user's cloud vault at the recorded location.
A trusted personal device copies it once and sets these modes. Vault access or
any enrolled host's fleet keys permit reading the repository and decrypting all
payloads; possession does not authorize installing every payload.

Discuss rotation and any history rewrite before acting. Retirement first removes
a reachable host's fleet directory, cluster key and tokens. Rotate both fleet
keys, update the vault, re-encrypt payloads and approvals, register the new deploy
key, bootstrap remaining hosts, then revoke the old deploy key. Unless the host
was wiped, end its service access too: reissue/revoke HF and GitHub tokens and
replace the cluster key/public key on nodes. Install replacement cluster keys
with `install-cluster-key --replace <old fingerprint>`. Old ciphertext in Git
history remains decryptable by the old identity.

## Bootstrap a server

Read [deployment configuration](private-deployment.md). Use the trusted
controller's private settings for clone URLs and the default GitHub account;
preserve an existing registered account.

Run from a trusted host holding the fleet directory and able to reach the
server as the user's account with `ssh -o BatchMode=yes`. The server requires
`git`, `python3`, `tar`, `gzip`, `sha256sum`, an SSH client and github.com
access; passwordless sudo is needed only for requested hosts-file work.

Use `<dotfiles>/scripts/bootstrap-remote <ssh-destination> [profile]` with
`--deployment-config <protected snapshot>` for the pinned settings. It streams
fleet keys, installs checksum-pinned `age` into `~/.local/bin` if needed, clones
dotfiles over HTTPS and the private repository with the deploy key, writes
`host-global` mode when absent, and registers the profile (default: short
hostname). One remote writer lock covers installed-identity verification, key
transfer, repository setup, and registration. An unverifiable or different
installed fleet identity blocks copying; rotation remains separately authorized.
Re-running repairs the same state. Run once per host sharing a home
to add each exact hostname to `host_profiles`.

If the inventory lacks a profile, read [inventory maintenance](private-inventory.md)
and add the remote `socket.gethostname()`, account, `development-server` role,
network-matching SSH context and hosts plan from its current `/etc/hosts`.
A short hostname differing from the node's `name` belongs in its `hostname`
field for the banner. Validate, encrypt, approve and publish using maintainer
write access, not the read-only deploy key.

Then issue that server's installation/environment-link and SSH stages from the
trusted host, with hosts-file work only when requested and `sudo -n` succeeds.
Read [installation](installation.md), [SSH synchronization](private-ssh.md), and
[hosts plans](private-hosts.md) for the selected stages. Each uses the server's
state, writer lock, identity and scripts; the trusted host sends commands and
retains no decrypted payloads. Bootstrap's explicit target authorization covers
this remote setup. Later refreshes run in agent sessions on the server, which
requires its own agent CLI login.
