# Phase 2 — Service Model Unification

## Goal

Expose one read-only V1 Service Model API over rule/_index.yaml and the
service metadata files already consumed by the V1 index loader.

## Contract

- src/engine/service_model/ is the public Service Model facade.
- src/engine/ingest/v1_index.py remains the low-level parser.
- No second service registry is introduced.
- generated/ is never an input.
- Service identity is deterministic and case-insensitive.
- Parent and child references are validated against the same catalogue.
- A stable fingerprint is available for downstream evidence binding.

## Parallelization boundary

This PR is self-contained. Phase 3 can implement its runtime boundary,
Phase 4 can implement semantic validation, and Phase 5 can implement release
orchestration while this PR is under CI. Merge order remains dependency-aware:
Phase 2, then Phase 3, then Phase 4, then Phase 5.

## Exit criteria

1. One public Service Model facade exists.
2. Existing V1 index parsing remains the underlying data source.
3. No duplicate SSOT is created.
4. Deterministic identity and fingerprint tests pass.
