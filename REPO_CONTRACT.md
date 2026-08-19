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
| Execution | CI validation of this repository only |
| Evidence | None |
| Receipt | None |
| Verification | Validation script and CI only |
| Governance | This contract and `GOVERNANCE.md` |
| Presentation | README and docs only |

## Release gate

A change is releasable only when:

1. Required contract, documentation, validation, test, and GitHub files exist.
2. The manifest and schema parse as UTF-8 JSON without duplicate object keys.
3. The manifest has only the required keys, with allowed types and values.
4. The manifest repository identity matches a required GitHub, explicit local,
   or Git remote identity source.
5. `REPO_CONTRACT.md`, `README.md`, and the creation decision match that identity.
6. `GOVERNANCE.md`, `SECURITY.md`, and every effective CODEOWNERS rule retain
   `owners.primary`, including the required catch-all rule.
7. Required files are regular files, and the baseline validation workflow
   exactly matches the reviewed read-only, credential-free, repository-local,
   action-pinned baseline.
8. A template repository contains no additional workflow.
9. The validator regression suite passes.
10. Secret-like material is not detected by the bootstrap guardrail.
11. CI passes for the relevant commit.

## Failure language

If the validation gate fails, the repository is not release-ready.

Do not describe a repository as verified, production-ready, compliant, or proof-producing unless the exact verifier, artifact, receipt, or proof path is named.

## Template use

When this repository is used to seed a new repository, the new repository must
complete `docs/customization-checklist.md` and pass its own validation workflow
before claiming its seed is complete.
