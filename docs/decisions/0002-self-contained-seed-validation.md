# 0002: Keep seed validation self-contained

Date: 2026-08-19

## Decision

After a commit-pinned checkout, the required bootstrap validation workflow runs
only repository-local validation logic with read-only GitHub contents permission.
It does not require an organization token, private repository checkout, external
verifier, signing service, or receipt generation path.

The bootstrap validator compares the workflow file with the reviewed canonical
baseline byte for byte. For the template repository, that file is the only
permitted workflow. This deliberately rejects execution-changing YAML variants,
skip conditions, additional steps, credentials, and other unreviewed workflow
surfaces.

## Reason

The workflow is copied into downstream repositories. A baseline that depends on
private WitnessOps repositories or an organization secret would fail closed for
new public repositories and would grant unnecessary credential access to a
structural seed check.

Repository-specific evidence or receipt workflows may be added later only when
their authority, credential scope, verifier, and operational value are explicit.

## Validation mechanism

```text
bash scripts/validate-repo.sh
.github/workflows/validate.yml
```

The command validates repository structure, identity consistency, manifest
shape, regression cases, and configured secret-like patterns.

A commit-pinned action update, including one proposed by Dependabot, must update
the workflow and the canonical validator value together in one reviewed pull
request. Downstream non-template repositories may add workflows only under a
repository-specific authority and credential review.

## Non-claim

Self-contained validation does not prove runtime correctness, security,
compliance, evidence authenticity, or production readiness.

## Status

Accepted.
