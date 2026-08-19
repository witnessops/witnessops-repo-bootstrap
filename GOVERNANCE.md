# Governance

## Governance scope

This repository governs only the WitnessOps repository bootstrap template.

It does not govern production infrastructure, customer evidence, receipt issuance, or verification outcomes.

## Change classes

| Change class | Examples | Required gate |
|---|---|---|
| Editorial | Typos, wording improvements | Validation pass |
| Template structure | Required file changes, new docs, script changes | Validation pass and owner review |
| Authority-impacting | Changes to `REPO_CONTRACT.md`, manifest semantics, release-gate semantics | Explicit owner review |
| Security-impacting | Secret scanning logic, workflow permissions, credential handling guidance | Explicit owner review |

## Owner boundary

Initial owner: `VaultSovereign`

Future team ownership may be added through CODEOWNERS and this file. Do not imply a team approval boundary until the team exists and is listed.

## Approval rule

A change can be merged when:

1. The validation workflow passes.
2. The change does not expand authority silently.
3. Any authority-impacting change is visible in the pull request body or commit message.
4. The repository contract remains accurate after the change.

## Baseline workflow rule

The required seed gate must remain self-contained and least-privilege. It may
check out this repository with read-only contents permission and run the named
local validator. It must not depend on an organization secret, private or
cross-repository checkout, external verifier, signing service, or receipt path.

The template workflow must match the reviewed canonical file exactly and remain
the template's only workflow. A pinned-action update must change the workflow
and the validator's canonical value together. A downstream repository may add a
workflow only after documenting that workflow's execution, permission,
credential, and authority boundary.

Adding any such dependency is both authority-impacting and security-impacting.
It requires explicit owner review and a separate repository-specific decision;
it is not part of the reusable baseline.

## Prohibited shortcuts

- Do not bypass validation and still claim the seed is complete.
- Do not introduce production credentials.
- Do not use this repo as customer evidence custody.
- Do not describe template validation as proof of runtime correctness.
- Do not make the reusable seed gate depend on organization credentials.

## Decision records

Durable repo decisions belong under `docs/decisions/`.
