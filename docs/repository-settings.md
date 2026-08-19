# Repository Settings

Source files cannot enforce these GitHub settings. An owner must configure and
verify them after the validation workflow has run at least once.

## Bootstrap repository

- Enable the GitHub template-repository setting for
  `witnessops-repo-bootstrap`.
- Keep `main` as the default branch.

## Default-branch rule

For `main`:

- Require changes through a pull request.
- Require at least one approval from the real owner boundary.
- Verify that the catch-all and any path-specific CODEOWNERS rules retain and
  resolve to the intended primary account or team, then require code-owner
  review.
- Dismiss stale approvals when new commits change the reviewed diff.
- Require conversation resolution.
- Require the `Validate repository contract` status check.
- Block force pushes and branch deletion.
- Keep bypass access limited to an explicitly documented emergency owner path.

## Public repository safeguards

- Keep secret scanning and push protection enabled where GitHub provides them.
- Enable GitHub private vulnerability reporting.
- Keep dependency update pull requests enabled for the checked-in Dependabot
  configuration.
- Use the repository security-reporting path for sensitive reports; do not put
  credentials, customer data, or private evidence in public issues.

Record any deliberate exception in a repository-specific decision. Passing the
source validator does not prove the GitHub organization, CODEOWNERS resolution,
ruleset, or security settings are active.
