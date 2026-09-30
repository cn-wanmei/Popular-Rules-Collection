# Icon V6 R5 Cutover — Final

**Date:** 2026-09-30  
**Default provider:** `v6`  
**Active dist release:** `icon-2026.09.30.clean1`  
**Manifest:** `manifests/icon-2026.09.30.clean1.json`  
**Canonical Collection service universe:** 394

## Verified production state

- Canonical services: **394/394**
- Production orphan entries: **0**
- Variant matrix: **8 styles × 128/256 = 16 per service**
- Variant records: **6304**
- Physical object closure: **PASS / 0 missing**
- Strict V6 manifest gate: **PASS**
- First clean release-writer build-and-gate: **PASS**
- First clean release-writer publish: **PASS**
- `ai` canonical service: **present**
- Independent V6 rollback: `icon-2026.09.30.clean1-rb1`

## V5 state

V5 is no longer a production dependency. `config/icon_v6.yaml` now has `fallback_to_v5: false` and the active resolver is V6-only.

Physical V5 assets are retained only until the retirement-gate commit is recorded. They are not read by production configuration.

## Final retirement sequence

1. clean1 production verified;
2. independent V6 rollback published;
3. V5 fallback disabled;
4. Collection retirement gate executes;
5. delete `assets/icons/v5`;
6. remove the now-obsolete retirement workflow;
7. rerun Collection validation and publish gates.

> V5 runtime implementation and V5 client resolver have now been removed from the production codebase. The physical `assets/icons/v5` archive remains only for the final gated deletion.

> Retirement gate evidence check is deterministic and uses the exact final clean1 state.

> Retirement gate uses sparse checkout because the Collection repository contains a large historical V5 tree; this does not change the retirement criteria.

> The final retirement gate uses non-cone sparse-checkout to avoid materializing the large legacy V5 tree.

> Final V5 retirement gate is repository-independent and validates the live main tree directly.
