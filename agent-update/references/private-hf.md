# Install the approved HF payload

Read [private synchronization](private-sync.md) before an explicitly requested
HF setup, repair or synchronization. Use only the enrolled host's verified
`hf-token` payload at the pinned revision; fleet-key possession or a generic
refresh does not authorize installation or rotation.

Use the installed `hf` runtime and its `HF_HOME`/token-path settings. Check
process token overrides without printing values. With pipe failure checking,
pipe verified ciphertext through `age --decrypt --identity <local identity>`
directly into `env -u HF_TOKEN -u HUGGING_FACE_HUB_TOKEN
<dotfiles>/scripts/install-hf-credential`. Override removal applies only to the
installer child; preserve the caller's environment.

The installer validates the token, locks the credential store, backs up replaced
files, uses standard HF library paths, enforces 0600, and checks `hf auth whoami`
without token overrides. Inspect its structured result. An interrupted library
write may need recovery from the private backup, not a blind retry. Apply the
common recorded-host lock reclamation and backup-retention rules.

Record verification and payload revision/digest without token values or plaintext
hashes. A current credential must cause no write. Failure leaves synchronization
incomplete; preserve recovery evidence and report the prerequisite or recovery.
