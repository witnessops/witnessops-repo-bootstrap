# Authority Boundary

## Purpose

This document separates the authority planes for the repository bootstrap template.

The template may define a starting repo contract. It does not grant runtime, evidence, receipt, verification, or governance authority to repositories that use it.

## Authority planes

| Plane | Meaning | Authority in this repo |
|---|---|---|
| Source | Files committed to GitHub | Yes |
| Execution | Code or workflows operating against runtime systems | No, except CI validation of this repo |
| Evidence | Captured operational/customer evidence | No |
| Receipt | Signed proof receipt issuance | No |
| Verification | Named checks that can be rerun | `scripts/validate-repo.sh` and `.github/workflows/validate.yml` |
| Governance | Rules for changing this template | `REPO_CONTRACT.md`, `GOVERNANCE.md`, CODEOWNERS |
| Presentation | Public explanation of the template | README and docs |

## Trust assumptions

- GitHub stores the source and commit history.
- GitHub Actions executes the validation workflow.
- The validation script checks structure and basic secret-like patterns only.
- The template consumer must update placeholder identity fields when creating a new repo.

## Failure modes

- Required files missing.
- Manifest invalid or incomplete.
- Repo class outside the allowed enum.
- Status outside the allowed enum.
- Authority block incomplete.
- Secret-like material detected by the bootstrap guardrail.
- Template used without replacing repo identity fields.

## Non-claims

Passing the bootstrap validation does not prove that a repository is secure, production-ready, compliant, or proof-producing.

It only proves that the seed contract files are present and that the local validator did not detect the configured structural failures.
