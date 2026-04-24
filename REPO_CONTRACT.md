# Repo Contract

## Repo identity

Repo: `witnessops-repo-bootstrap`  
Class: `template`  
Status: `seeded`

## Purpose

This repository provides the starting contract for new WitnessOps repositories.

It exists to prevent repositories from acquiring operational, proof, customer, or governance authority by accident.

## This repo is authority for

- Baseline repository seed structure.
- Baseline repository manifest shape.
- Baseline validation gate.
- Baseline authority-boundary language.
- Baseline release-gate language.

## This repo is not authority for

- Production runtime state.
- Customer evidence custody.
- Signed receipt issuance.
- Offline verification outcomes.
- Runtime secret custody.
- Commercial pricing or packaging.
- Legal, audit, or compliance determinations.

## Authority separation

| Plane | Authority in this repo |
|---|---|
| Source | Files committed to this repository |
| Execution | None |
| Evidence | None |
| Receipt | None |
| Verification | Validation script and CI only |
| Governance | This contract and `GOVERNANCE.md` |
| Presentation | README and docs only |

## Release gate

A change is releasable only when:

1. `repo.manifest.json` exists.
2. `repo.manifest.json` parses as JSON.
3. Required repo contract files exist.
4. Required documentation files exist.
5. Required GitHub workflow files exist.
6. Secret-like material is not detected by the bootstrap validation script.
7. CI passes.

## Failure language

If the validation gate fails, the repository is not release-ready.

Do not describe a repository as verified, production-ready, compliant, or proof-producing unless the exact verifier, artifact, receipt, or proof path is named.

## Template use

When this repository is used to seed a new repository, the new repository must replace placeholder identity fields before claiming its own seed is complete.
