# Phase 8 — Legacy Delete

## Goal
Provide the final explicit operator action for deleting database/services after the complete V1 migration gate passes.

## Safety contract
- No CI workflow deletes Legacy automatically.
- The final migration gate must be PASS.
- V1 Canonical must be the active Source of Truth.
- Final evidence must be bound to the current HEAD.
- The target is exactly database/services.
- A separate explicit operator approval is required.
- Missing, stale or malformed evidence fails closed.

## Parallelization boundary
Phase 8 can be implemented and tested independently because the final gate already serializes the runtime evidence from Phases 4–7. The PR adds only the guarded execution boundary.

## Execution
`python scripts/legacy_delete.py --approve` is a manual operator action after verifying the final migration gate. It is never called by the production build or publish workflows.

## Exit criteria
1. Unauthorized deletion is impossible through the entrypoint.
2. Wrong target, wrong SoT, stale HEAD or non-PASS gate is refused.
3. No automatic deletion path is introduced.


## Closure hardening

The final deletion path is two-stage:

1. The production V3 run must already have Phase 4 semantic validation, Phase 6 observation, and Phase 7 finalization as hard gates.
2. A current-HEAD closure gate is regenerated in a fresh checkout and kept as workflow artifact evidence. It is deliberately not committed before deletion, because committing a gate changes HEAD and would invalidate a current-HEAD-bound deletion authorization.
3. The workflow rechecks `origin/main` immediately before deletion. Any concurrent commit aborts the deletion.
4. Deletion is triggered only by the explicit operator approval marker `.github/phase8-operator-approval/APPROVED` with the exact approval text required by the workflow.
5. After successful deletion, `reports/v1/PHASE8_DELETION_FINAL.json` records the bound pre-delete HEAD and the explicit approval.

The repository's checked-in migration gate remains build evidence. The closure workflow's current-HEAD gate is the authorization evidence used for the destructive action.
