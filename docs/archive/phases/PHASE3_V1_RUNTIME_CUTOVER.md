# Phase 3 — V1 Runtime Cutover

## Goal
Make runtime lookup explicit: indexed V1 service paths resolve only inside rule/.
Published output is never used as runtime input.

## Contract
- SoTResolver resolves service names and explicit V1 relative paths.
- Relative V1 paths must begin at rule/ and cannot traverse upward.
- V1RuntimeCutover validates every indexed entry that declares a path.
- The gate is read-only and fails closed for unresolved entries.

## Parallelization boundary
This PR is independent of the Phase 2 branch. It starts from the same Phase 1
merge base and can run its own focused CI before merge.

## Exit criteria
1. Nested V1 rule paths resolve deterministically.
2. Path traversal outside rule/ is rejected.
3. The cutover gate fails closed for unresolved indexed paths.
