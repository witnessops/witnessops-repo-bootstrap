# Changelog

All durable changes to this repository should be recorded here.

## 0.2.0 - 2026-08-19

### Hardened

- Made the required CI gate self-contained, read-only, credential-free, and
  independent of private repositories or an external verifier.
- Added exact manifest, repository-identity, owner-parity, and workflow-boundary
  validation with standard-library regression tests.
- Closed validator bypasses by rejecting duplicate JSON keys, required-file
  symlinks, unsupported schema keywords, missing or overridden identity sources,
  ineffective CODEOWNERS rules, workflow skip or syntax variants, and extra
  template workflows.
- Defaulted the template to no allowed secret storage or proof surfaces.
- Added a repository customization checklist, repository-standard issue form,
  controlled issue intake, repository-settings checklist, contribution guide,
  dependency-update policy, and decision record for the self-contained baseline.

## 0.1.0 - 2026-04-24

### Added

- Seeded repository bootstrap contract.
- Added governance and security boundaries.
- Added manifest, schema, validation script, and CI gate.
- Added authority-boundary, operating-model, release-gate, and creation decision docs.
