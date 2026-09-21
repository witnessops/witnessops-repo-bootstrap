# 0004: Shared context pointer for agent briefing

Date: 2026-09-21

## Decision

Add a short start section to the existing `AGENTS.md` that points agents doing
WitnessOps work to the current organization context and its applicable pointers.
Keep local instructions in force, work through actual approved scope without
repeated assent, and handle unavailable shared context as a named limitation.

## Reason and authority

The founder approved the two-repository briefing patch in the originating
conversation on 21 September 2026. The central
[founder-mobile operating decision](https://github.com/witnessops/.github/blob/main/repository-governance/decisions/FOUNDER_MOBILE_OPERATING_MODEL_20260921.md)
records the operating direction. This implements its briefing pointer only;
it does not authorize unrelated repository administration or runtime work.

## Boundary

The existing seed process already copies `AGENTS.md`; no new required seed file,
workflow, credential, network validation dependency or cross-repository checkout
is introduced. This record is template-local, not an addition to the required
seed inventory. Manifest, contract, owner, release and validation semantics stay
unchanged. Private central content is not copied into the public template.

Unavailable context does not authorize a bypass: pause actions dependent on
missing authority while continuing unrelated safe work and the local gate.
No deployment, new repository, access change or organization-wide rollout follows.

## Validation and limits

Use the existing `bash scripts/validate-repo.sh` gate, inspect the exact diff and
read merged source back. Record actual results and source refs on the PR.
A link and a passing structural gate do not prove an agent loaded or followed the
briefing. A separate fresh-agent exercise would be needed to establish that.

## Status

Accepted for the documentation-only briefing scope.
