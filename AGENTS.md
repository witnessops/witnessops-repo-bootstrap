# AGENTS.md

## Scope

This repository is the template foundation for new WitnessOps repositories.

It seeds new repositories with a bounded authority contract, machine-readable manifest, validation gate, governance language, and release checklist before feature work begins.

## Authority

This repository is authority for:

- the minimum files required for a WitnessOps repository seed
- the default repo manifest shape
- the default validation script used by newly seeded repositories
- baseline language for authority, execution, evidence, proof, verification, governance, and presentation boundaries

This repository is not:

- product runtime
- verifier
- proof issuer
- customer evidence store
- secret store
- production authority

## Required Command

Run the repository validation gate before claiming a local patch is ready:

```bash
bash scripts/validate-repo.sh
```

This command runs the structural validator and its regression suite. The
required CI workflow invokes the same command without organization credentials,
private repository checkouts, an external verifier, signing, or receipt
generation. Passing it does not prove seeded repos are verified,
production-ready, compliant, or proof-producing.

## Completion Evidence

Every Codex implementation lane must report:

1. files changed
2. commands run
3. validation result
4. template contract impact
5. remaining risks
6. suggested PR title/body when PR preparation is in scope
7. claims not made

## Do-Not Rules

- Do not add secrets, production credentials, private keys, customer evidence, live evidence, tokens, or signing material.
- Do not claim this repository is product runtime, verifier, proof issuer, customer evidence store, secret store, or production authority.
- Do not claim a seeded repository is verified, production-ready, compliant, or proof-producing unless the exact verifier, artifact, receipt, or proof path is named.
- Do not change seeded repository authority language casually; template wording affects downstream repo boundaries.
- Do not widen validation, release, or governance claims beyond the named command and artifacts.
- Do not add a credential or cross-repository dependency to the reusable baseline validation workflow.
- Do not change the canonical validation workflow without updating its validator
  value, regression coverage, decision record, and authority-impact review.
- Do not add another workflow while the repository class is `template`.
- Do not modify files outside the approved lane scope.

## Release Language

A repository seeded from this template may be called `seeded` only after the validation gate passes.

Do not call any repository verified, production-ready, compliant, or proof-producing unless the exact verifier, artifact, receipt, or proof path is named.
