# 0003: Scripted seeding path and template-independent regression suite

Date: 2026-08-20

## Decision

Add `scripts/seed-new-repo.sh` and `scripts/seed_new_repo.py` as the supported
path for creating a new repository from this template. The script copies
exactly the documented seeded inventory, rewrites the manifest, contract,
README title, creation decision, governance, security, and CODEOWNERS identity
fields, and then runs the copied validation gate with the new repository
identity before reporting success. It fails closed if any rewrite or the gate
fails.

Make `tests/test_validate_repo.py` read the repository identity, class, and
primary owner from `repo.manifest.json` instead of hardcoding the template
values, and run the template-only workflow-inventory regression only in
template-class repositories, so the copied gate passes in a customized seeded
repository.

## Reason

The regression suite previously hardcoded the template identity and owner, so
a repository copied from this template failed its own required gate as soon as
the customization checklist was completed. Manual copying also invited drift
between the documented seeded inventory and what was actually copied.

## Boundary

The seeding script is template tooling only. It is not part of the seeded
inventory. It stores no credentials, does not create the GitHub repository,
does not apply `docs/repository-settings.md`, and does not complete the manual
customization-checklist items.

## Validation mechanism

```text
bash scripts/validate-repo.sh
.github/workflows/validate.yml
```

The seeding script additionally runs the same command inside the newly seeded
repository with `WITNESSOPS_EXPECTED_REPO_ID` set to the new identity, and the
template regression suite proves an end-to-end seed passes that gate.

## Non-claim

A scripted seed is structural only. It does not make a repository verified,
production-ready, compliant, or proof-producing.

## Status

Accepted.
