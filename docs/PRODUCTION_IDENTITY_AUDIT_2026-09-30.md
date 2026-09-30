# Icon Production & Identity Audit — 2026-09-30

## Canonical identity

Popular-Rules-Collection `rule/_index.yaml` is the sole service identity authority.

- canonical service count: **394**
- canonical source blob: `493eb3bcbb9e69c3067adeed336cc0e2566537a1`
- canonical `ai` entry: `special/ai/ai.yaml`, provider `special`

## Clean V6 release

The first clean V6 release-writer publication is verified:

- release: `icon-2026.09.30.clean1`
- canonical entries: **394/394**
- orphan entries: **0**
- missing canonical services: **0**
- variant matrix: **8 styles × 128/256**
- variant records: **6304**
- physical object closure: **6304 referenced variants, 0 missing**
- strict V6 manifest gate: **PASS**
- release-writer build-and-gate: **PASS**
- release-writer publish: **PASS**

The missing `ai` identity was materialized from the controlled generated seed and included in clean1.

## Historical/orphan cleanup

Icon production Registry/state was reduced from 482 identities to the 394 canonical Collection services.

The removed 89 historical/orphan identities are archived in the Icon repository audit record:

`reports/orphaned-production-identities-2026-09-30.json`

Classification includes provider aggregates, domestic aggregate/category records, and historical/Collection-missing identities. They are no longer production service identities.

## Collection cutover

This finalization branch changes Collection to:

```yaml
provider: v6
v6:
  release_id: icon-2026.09.30.clean1
  manifest_path: manifests/icon-2026.09.30.clean1.json
  fallback_to_v5: false
rollback:
  provider: v6
  release_id: icon-2026.09.30.r14.1
```

The V6 resolver is fail-closed and no longer falls back to V5.

## V5 retirement

The finalization branch removes:

- `assets/icons/v5/`
- `scripts/icon_system_v5.py`
- `scripts/icon_resolver_v5.py`
- `scripts/icon_v5_renderers/`
- `config/icon_v5.yaml`
- `config/icon_v5_clients.yaml`
- `tests/test_icon_system_v5.py`

The V5 retirement workflow is retained only as a non-destructive verification gate.

## Verification state

Before merge, the remaining required evidence is:

1. Collection PR CI completes successfully after the final resolver test fixture correction.
2. V5 retirement gate completes successfully on the final branch head.
3. Collection PR #279 is merged.
4. Post-merge audit confirms the V5 tree/runtime files are absent from `main`.

No production path is allowed to recreate the V5 tree.
