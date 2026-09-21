# AGENTS.md

## Start here for WitnessOps work

Before material WitnessOps work, read the current
[ChatGPT context entrypoint](https://github.com/witnessops/.github/blob/main/CHATGPT_CONTEXT.md)
and follow only the canonical pointers needed for the task, including its linked
founder-mobile operating decision. This is orientation, not execution authority.
Keep this file and applicable repository/scoped instructions in force; resolve
conflicts before the affected action rather than silently overriding a contract.

Establish the goal, approved actions and exclusions, existing component, current
ref/open work, checks and stop conditions before a write or execution. Retrieve
available answers instead of asking the founder to repeat them. Continue routine
work and authorized delivery within that scope without repeated approval; ask
only for a material new decision, a mandatory human-only step or an unresolved
blocker. Preserve existing checks and owner/recovery access.

Use existing authorized access to read shared context. If it is unavailable,
state the missing source and limitation, pause only work that depends on missing
authority, and continue unrelated safe work and self-contained validation. Do not
invent authority, request secrets or change access controls to obtain context.
Never fetch private context from CI or add credentials, cross-repository checkouts
or a network prerequisite to the seed gate. Do not copy the organization inventory
or central policy text into each seed. This pointer remains agent guidance only.

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
