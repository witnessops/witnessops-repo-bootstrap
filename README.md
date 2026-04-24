# witnessops-repo-bootstrap

Template foundation for new WitnessOps repositories.

This repository is not a product runtime, verifier, proof issuer, or customer evidence store. Its job is to seed new repositories with a bounded authority contract, machine-readable manifest, validation gate, governance language, and release checklist before feature work begins.

## What this repo is authority for

- The minimum files required for a WitnessOps repository seed.
- The default repo manifest shape.
- The default validation script used by newly seeded repositories.
- The baseline language for authority, execution, evidence, proof, verification, governance, and presentation boundaries.

## What this repo is not authority for

- Production infrastructure state.
- Runtime secret custody.
- Customer evidence custody.
- Signed receipt issuance.
- Verification outcomes.
- Commercial claims.
- Compliance determinations.

## Seeded repo contract

A new WitnessOps repo should begin with:

```text
README.md
REPO_CONTRACT.md
GOVERNANCE.md
SECURITY.md
CHANGELOG.md
LICENSE
repo.manifest.json
schemas/repo.manifest.schema.json
scripts/validate-repo.sh
.github/workflows/validate.yml
.github/CODEOWNERS
.github/pull_request_template.md
docs/authority-boundary.md
docs/operating-model.md
docs/release-gates.md
docs/decisions/0001-repo-created.md
```

## Validation

Run locally:

```bash
bash scripts/validate-repo.sh
```

CI runs the same validation on pushes to `main` and pull requests.

## Repo classes

Allowed starting classes:

```text
proof-component
verifier
catalogue
site
operator-tool
schema-registry
sample-cases
docs
integration-bridge
template
```

## Release language

A repo seeded from this template may be called `seeded` only after the validation gate passes.

Do not call a repository verified, production-ready, compliant, or proof-producing unless the exact verifier, artifact, receipt, or proof path is named.

## Operator rule

Use this repository to create a clean starting boundary. Do not let template files imply authority that the new repository does not actually hold.
