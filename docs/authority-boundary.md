# Authority Boundary

## Purpose

This document separates the authority planes for the repository bootstrap template.

The template may define a starting repo contract. It does not grant runtime, evidence, receipt, verification, or governance authority to repositories that use it.

## Authority planes

| Plane | Meaning | Authority in this repo |
|---|---|---|
| Source | Files committed to GitHub | Yes |
| Execution | Code or workflows operating against runtime systems | CI validation of this repository only |
| Evidence | Captured operational/customer evidence | No |
| Receipt | Signed proof receipt issuance | No |
| Verification | Named checks that can be rerun | `scripts/validate-repo.sh` and `.github/workflows/validate.yml` |
| Governance | Rules for changing this template | `REPO_CONTRACT.md`, `GOVERNANCE.md`, CODEOWNERS |
| Presentation | Public explanation of the template | README and docs |

## Trust assumptions

- GitHub stores the source and commit history.
- GitHub Actions executes the validation workflow.
- The validation workflow checks out only this repository with read-only contents
  permission and runs repository-local code.
- The validation script checks manifest shape, expected repository identity,
  cross-file identity, effective catch-all ownership, canonical workflow bytes,
  regression cases, and configured secret-like patterns.
- The template consumer must complete `docs/customization-checklist.md` when
  creating a new repository.

## Failure modes

- Required files missing.
- Manifest invalid or incomplete.
- Repo class outside the allowed enum.
- Status outside the allowed enum.
- Authority block incomplete.
- Repository, contract, README, or creation-decision identity mismatch.
- Owner mismatch or an overriding CODEOWNERS rule that drops the primary owner.
- Baseline workflow requests write access, credentials, or another repository.
- Baseline workflow is skipped, changed, or accompanied by another template
  workflow.
- Secret-like material detected by the bootstrap guardrail.
- Template used without replacing repo identity fields.

## Non-claims

Passing the bootstrap validation does not prove that a repository is secure, production-ready, compliant, or proof-producing.

It only shows that the named validator and regression cases did not detect the
configured structural failures in the tested commit.

The source validator checks the repository name, not GitHub organization
membership or live repository settings. An owner must separately verify the
organization, effective ruleset, review boundary, and security settings.
