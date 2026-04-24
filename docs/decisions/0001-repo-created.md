# 0001: Repository created

Date: 2026-04-24

## Decision

Create `witnessops-repo-bootstrap` as the reusable bootstrap template for new WitnessOps repositories.

## Reason

New repositories should not begin as loose file collections. They need a repo contract, manifest, validation gate, governance boundary, security boundary, and release language before feature work begins.

## Boundary

This repository is authority for the bootstrap template only.

It is not authority for production runtime state, customer evidence, receipt issuance, verification outcomes, or compliance claims.

## Validation mechanism

The named validation mechanism is:

```text
bash scripts/validate-repo.sh
.github/workflows/validate.yml
```

## Status

Accepted.
