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
