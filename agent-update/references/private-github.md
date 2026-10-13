# Install the GitHub account credential

Read [private synchronization](private-sync.md) before an explicitly requested
GitHub credential setup, repair or synchronization. Require registered
`github_identity` and `github_account`, and independently approved
`github-token.age` at the pinned revision. Fleet-key possession alone does not
authorize account access.

## Validate before writing

Clear `GH_TOKEN`, `GITHUB_TOKEN` and enterprise-token overrides only in installer
and verification children, without printing values. Inspect installed
`gh auth login --help`; use official documentation if behavior differs.
Validate the candidate with `gh api --hostname github.com user`, injecting only
that token into the child environment. Require a case-insensitive
`github_account` match before any credential write. Tokens never enter argv or
Git URLs. Inspect/preserve existing accounts; an unexpected active account
requires authorized switching.

Under the shared-home writer lock, back up the resolved standard gh and affected
Git configurations, modes included (backup directories 0700, files 0600).
Reject unknown symlinks/concurrent changes. Compare the stored token in memory
to avoid unchanged writes. Pipe the candidate into
`gh auth login --hostname github.com --git-protocol https --with-token`.
A headless server's enrollment authorizes `--insecure-storage` only when no
secure store is configured: enforce config-directory 0700 and `hosts.yml` 0600
and report local plaintext storage. Preserve existing secure storage; an account
entry without a local token may use another shared-home host's keyring and must
be investigated. Preserve unrelated hosts/accounts and AI CLI credentials.

## Configure and verify access

`gh auth setup-git --hostname github.com` affects GitHub.com HTTPS access for
the whole account, including existing repositories. Back up and report replaced
GitHub helpers. Run it, then verify the registered account with `gh api
--hostname github.com user` without overrides. Verify required private-repository
HTTPS reads using `GIT_TERMINAL_PROMPT=0`: use the inventory verification target
or an HTTPS rendering of its registered URL without changing origin.

Configure HTTPS only for approved GitHub repositories. Preserve SSH routes/keys
and the private-sync checkout's independent read-only bootstrap authentication.
Enrolled servers require its SSH origin and explicit deploy-key command; reject
an HTTPS bootstrap origin that the global helper could capture. HTTPS helpers
do not authenticate SSH remotes. Access remains limited by token scopes,
organization authorization and user rights. For user-owned harness repositories
with read-only SSH fetch keys, set HTTPS `remote.origin.pushurl` and inspect push
permission through `gh`; this survives submodule URL synchronization. Preserve
vendor origins and never create external objects merely to test write access.

Record account, private read verification and payload revision/digest without
token values or plaintext hashes. Authentication/scope failures block credential
success. Use common hash-guarded recovery after post-write failure and preserve
backups. Do not log out or revoke a shared token to repair one host. Rotation
requires an approved replacement payload and verification of authorized members
before revoking the old credential.
