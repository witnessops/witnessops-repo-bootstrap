# Release Gates

## Gate 0: identity present

Required files must exist:

- `README.md`
- `REPO_CONTRACT.md`
- `GOVERNANCE.md`
- `SECURITY.md`
- `repo.manifest.json`
- `schemas/repo.manifest.schema.json`

## Gate 1: manifest parses

`repo.manifest.json` and `schemas/repo.manifest.schema.json` must parse as valid JSON.

## Gate 2: manifest contract present

The manifest must include the required top-level fields and the required authority fields.

## Gate 3: allowed enum values

`repo_class` and `status` must use values allowed by the schema.

## Gate 4: ownership present

`owners.primary` must be populated.

## Gate 5: basic secret guardrail

The validation script must not detect configured secret-like patterns in repository files.

## Gate 6: CI pass

The GitHub Actions validation workflow must pass for the relevant commit.

## Completion language

If all gates pass, the repository seed may be described as structurally seeded.

Do not describe the repository as production-ready, secure, compliant, or proof-producing based only on these gates.
