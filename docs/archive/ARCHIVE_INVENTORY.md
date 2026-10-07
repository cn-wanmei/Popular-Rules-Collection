# Process artifact archive inventory

Updated **2026-10-07** after dependency scan of `build.yml` / `publish.yml` / scripts.

## Rule

Do **not** delete or relocate any path still referenced by workflows or production scripts without updating callers in the **same** PR.

## CI-held — KEEP

| Asset | Consumer |
|-------|----------|
| `scripts/phase_j_p0_service_evidence.py` | `build.yml` |
| `config/p0_materialization.yaml` | phase_j evidence script |
| `config/p0_service_identity.yaml` | phase_j evidence script |
| `scripts/p0_batch01_semantic_overlap_audit.py` | `publish.yml` |
| `config/p0_batch01_semantic_audit.yaml` | batch01 audit |
| `config/p0_batch01_overlap_audit.yaml` | batch01 audit |
| `config/p0_batch01_snapshots/**` | paths in batch01 semantic yaml |
| `scripts/legacy_*.py` | until `docs/LEGACY_STATUS.md` Phase 8 PASS |
| `database/` | until Phase 8 PASS |

## Archive candidates (verify with rg before move)

- `config/phase_i_*` … `phase_o_*`, `phase_j_p0_batch_plan.yaml`
- `config/v1_final_migration_gate.yaml`, `canonical_root_migration.yaml`
- `config/p0_batch02_*` … `p0_batch04_*` (+ snapshot dirs)
- `config/p0_geosite_*`, `config/p0_source_*` (except any still imported)

Target: `docs/archive/phases/config/` and `docs/archive/phases/snapshots/`.

## Completed

- [x] Root freeze stubs removed (#294)
- [x] KEEP map locked (this file)
- [x] Retention weekly dry-run workflow on main
- [x] entity_coverage_report.py on main
- [ ] Physical move of archive-candidate trees (optional; large snapshots)

## Status

2026-10-07: dependency map locked; retention + entity report landed on main.
