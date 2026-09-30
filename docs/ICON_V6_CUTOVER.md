# Icon System V6 — Final Clean Cutover

**Date:** 2026-09-30  
**Default provider:** `v6`  
**Active immutable release:** `icon-2026.09.30.clean1`  
**Manifest:** `manifests/icon-2026.09.30.clean1.json`  
**Canonical Collection service universe:** 394

## Verified release

The first clean V6 release was built and published by the Icon Repository release writer.

- canonical entries: **394/394**
- production orphan entries: **0**
- variants: **8 styles × 128/256**
- variant records: **6304**
- physical referenced objects missing: **0**
- strict V6 manifest gate: **PASS**
- release writer build-and-gate: **PASS**
- release writer publish: **PASS**

The missing `ai` canonical service was completed in the exact clean state snapshot and materialized into clean1.

## Identity boundary

`Popular-Rules-Collection/rule/_index.yaml` is the sole service identity authority.

`Popular-Rules-Icon` consumes the canonical `service_id`, `display_name`, and `provider` and must not invent, rename, merge, or reinterpret services.

The 89 historical/orphan production identities were removed from production Registry/state and archived in the Icon repository audit record.

## Cutover

Collection now uses:

```text
provider: v6
release_id: icon-2026.09.30.clean1
fallback_to_v5: false
rollback:
  provider: v6
  release_id: icon-2026.09.30.r14.1
```

V5 is no longer part of production or rollback.

## V5 retirement

The V5 local asset tree is retired and must be deleted from Collection after the final retirement gate passes. V5 code and active automation are removed or retained only as historical documentation where required for audit.

## Resolver

The Collection V6 resolver is fail-closed. Missing or invalid V6 assets return an error; it never falls back to a Collection-local V5 asset.

## Completion state

All eight retirement conditions are satisfied by the clean1 evidence chain. The final action is to execute the retirement gate and delete `assets/icons/v5` and the obsolete V5 runtime/test implementation.
