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
.gitignore
AGENTS.md
CONTRIBUTING.md
README.md
REPO_CONTRACT.md
GOVERNANCE.md
SECURITY.md
CHANGELOG.md
LICENSE
repo.manifest.json
schemas/repo.manifest.schema.json
scripts/validate-repo.sh
scripts/validate_repo.py
tests/test_validate_repo.py
.github/workflows/validate.yml
.github/CODEOWNERS
.github/dependabot.yml
.github/pull_request_template.md
.github/ISSUE_TEMPLATE/config.yml
.github/ISSUE_TEMPLATE/repository-standard-gap.yml
docs/authority-boundary.md
docs/customization-checklist.md
docs/operating-model.md
docs/release-gates.md
docs/repository-settings.md
docs/decisions/0001-repo-created.md
docs/decisions/0002-self-contained-seed-validation.md
```

## Customize before calling a repo seeded

A copied repository still describes this bootstrap until its identity,
authority, ownership, and purpose are replaced. Complete the
[repository customization checklist](docs/customization-checklist.md) before
using `seeded` status.

## Validation

With Bash and Python 3.10 or newer, run locally:

```bash
bash scripts/validate-repo.sh
```

The gate validates regular required files, duplicate-free exact manifest shape,
trusted repository identity, effective cross-file ownership, the canonical
least-privilege workflow, configured secret-like patterns, and its regression
suite. The template rejects additional workflow files until a copied repository
changes class and documents its own workflow authority.

CI runs the same gate on pushes to `main`, pull requests, and manual dispatch.
The baseline workflow uses no organization secret, private repository checkout,
external verifier, signing service, or proof receipt path.

GitHub settings are a separate owner-operated gate. Apply
[`docs/repository-settings.md`](docs/repository-settings.md) after the validation
check exists.

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
