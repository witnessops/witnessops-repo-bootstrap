# Contributing

Keep changes bounded to this repository bootstrap and make authority impact easy
to review.

1. Open one focused branch and pull request per change.
2. Select the change class in the pull request template.
3. State any authority or security impact explicitly.
4. Update the changelog and decision records when the reusable standard changes.
5. Run `bash scripts/validate-repo.sh` and report the exact result.
6. Request review from the owner boundary named in CODEOWNERS.

The baseline workflow is intentionally canonical. If a pinned action is updated,
change `.github/workflows/validate.yml` and `CANONICAL_VALIDATION_WORKFLOW` in
`scripts/validate_repo.py` together. Any other workflow change requires an
explicit decision describing its execution, permissions, credentials, and
authority impact.

Use the repository-standard issue form for non-sensitive gaps. Follow
`SECURITY.md` for security concerns. Never include secrets, credentials,
customer data, private evidence, or production material in an issue or pull
request.
