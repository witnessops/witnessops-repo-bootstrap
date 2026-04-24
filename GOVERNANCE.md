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

## Prohibited shortcuts

- Do not bypass validation and still claim the seed is complete.
- Do not introduce production credentials.
- Do not use this repo as customer evidence custody.
- Do not describe template validation as proof of runtime correctness.

## Decision records

Durable repo decisions belong under `docs/decisions/`.
