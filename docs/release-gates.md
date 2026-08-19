# Release Gates

## Gate 0: required inventory

Every file named by `scripts/validate_repo.py` must exist. This includes the
contract, manifest and schema, governance and security guidance, validation
workflow, local validator, regression tests, contribution surfaces, and
repository-settings checklist.

The README seeded-repository inventory must list that exact file set without
duplicates or undocumented additions.

## Gate 1: exact manifest shape

`repo.manifest.json` and its schema must parse as UTF-8 JSON without duplicate
object keys. The manifest must contain exactly the supported top-level and
nested keys. Required strings must be non-empty; arrays must contain unique
non-empty strings; class and status must use allowed values; and `forbidden`
must not be empty.

## Gate 2: repository identity parity

The manifest `repo_id` must match, in priority order, `GITHUB_REPOSITORY`, the
explicit local `WITNESSOPS_EXPECTED_REPO_ID` value, or the configured Git origin.
An explicit local value cannot override GitHub's CI repository identity. The
identity must also match `REPO_CONTRACT.md`, the README title, and the repository
creation decision. Validation fails when no repository-identity source is
available. Contract class and status must match the manifest.

## Gate 3: ownership parity

`owners.primary` must match the initial owner in `GOVERNANCE.md` and
`SECURITY.md`. CODEOWNERS must contain an effective catch-all rule naming that
exact owner, and every additional rule must retain that owner. A comment or an
overriding path rule without the primary owner does not satisfy this gate.

## Gate 4: bounded template defaults

A repository with class `template` must default to no allowed secret storage and
no proof surfaces. A copied repository may change those fields only to describe
authority and surfaces it actually has.

## Gate 5: self-contained workflow

The required workflow must match the reviewed canonical self-contained baseline
exactly. The canonical file uses read-only contents permission, disables
persisted checkout credentials, runs `bash scripts/validate-repo.sh`, sets a
timeout, and pins checkout by full commit. Exact matching also rejects skip
conditions, extra steps, alternate YAML spellings, job-level overrides, secrets,
and unreviewed execution surfaces. A template repository may contain no other
workflow file.

Downstream non-template repositories may add workflows only after documenting
and reviewing their repository-specific authority and credential boundaries.

## Gate 6: secret-like material guardrail

The configured basic patterns must not find secret-like material in repository
files. This gate is intentionally bounded and is not a complete secret scan.

## Gate 7: regression suite

The standard-library unit tests must prove the valid baseline and customized
identity path pass, and representative missing-file, symlink, malformed or
duplicate-key manifest, stale identity, cross-file mismatch, ineffective owner,
secret-like material, workflow-override, and extra-template-workflow regressions
fail.

## Gate 8: CI pass

The GitHub Actions validation workflow must pass for the relevant commit. Apply
the required branch rule only after the check exists on the default branch.

## Completion language

If all gates pass, the repository seed may be described as structurally seeded.
Do not describe it as secure, production-ready, compliant, verified, or
proof-producing based only on these gates.
