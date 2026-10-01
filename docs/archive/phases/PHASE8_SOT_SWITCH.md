# Phase 8 — SoT Switch Record

**Date:** 2026-09-18  
**Decision:** `sot = v1_canonical`  
**Legacy deletion:** **NOT authorized** (`legacy_deleted = false`)

## Gate results

| Gate | Result |
|------|--------|
| intentional_registry_valid | PASS |
| coverage_100 | PASS (100%, registered=218, missing=0) |
| no_unexplained_removed | PASS (Phase 7, unexplained=0) |
| graph_acyclic | PASS (Phase 3.2) |
| golden_gate | PASS (Phase 4, 15/15 matched) |

## Phase details

### Phase 7 — Legacy vs V1
- Service-level comparison
- **Added:** 34 (intentional-only catalogue rows from P0)
- **Removed:** 0 unexplained
- All Added rows explained via `intentional_unmaterialized.yaml`

### Phase 3.2 — Graph
- `build_graphs(..., raise_on_cycle=True)` completed with no cycles
- Sparse edges when full metadata tree is not checked out; acyclicity holds

### Phase 4 — Golden
- All 15 golden service ids matched
- Structural coverage: Parent, Child, Aggregate, Domain-only, IP-only, Duplicate

## What this does **not** do

- Does **not** delete Legacy sources
- Does **not** set `allow_legacy_delete` operator approval for filesystem removal
- Production publish paths should treat **V1 Canonical** as Source of Truth going forward

## Next

1. Wire pipelines to prefer V1 Canonical when `sot=v1_canonical`
2. Observation window (seven-client + deterministic builds)
3. Only then: `request_legacy_delete(allow_legacy_delete=True)` + operator script
