## Pending-review contract

Use the current authenticated GitHub viewer's pending review only. Query the
PR and the viewer's reviews before writing:

- If no pending review exists, create one review containing the complete set
  of inline comments. Pass `HEAD_SHA` as the review commit and omit the review
  event so GitHub leaves it `PENDING`.
- If a pending review already exists on `HEAD_SHA`, preserve its existing
  comments and add the new comments to that review. Before adding anything,
  compare `path`, `line`, `side`, and `body` with existing pending comments and
  skip exact duplicates.
- If the viewer's pending review targets another commit, stop without changing
  it. Report that the existing review must be submitted or discarded before a
  review for `HEAD_SHA` can be created.

For a new review, use GitHub's create-review API or the GraphQL
`addPullRequestReview` mutation with all inline comments in one request and no
event. To extend an existing pending review, use the GraphQL
`addPullRequestReviewThread` mutation with its `pullRequestReviewId`; never use
the standalone review-comment endpoint, because that publishes immediately.
Keep the review body empty unless the user explicitly requests a pending
summary.

If extending a review fails after some threads were added, stop and report the
exact partial result. Leave every successful comment pending; do not delete the
review, retry comments whose outcome is uncertain, publish replacements, or
submit the partial review. Re-read the PR head after writing. If it changed
during the mutation window, report that the pending comments target the
recorded `HEAD_SHA` and require revalidation before submission.
