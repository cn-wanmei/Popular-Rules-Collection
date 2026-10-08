# Process artifact archive inventory

## CI-held — KEEP

| Asset | Consumer |
|-------|----------|
| `scripts/phase_j_p0_service_evidence.py` | `build.yml` |
| `config/p0_materialization.yaml` | phase_j |
| `config/p0_service_identity.yaml` | phase_j |
| `scripts/p0_batch01_semantic_overlap_audit.py` | `publish.yml` |
| `config/p0_batch01_*` + snapshots | batch01 |
| `scripts/legacy_*.py` / `database/` | until Phase 8 PASS |

## Removed from config/ (2026-10-08)

See [phases/ARCHIVED_2026-10-08.md](phases/ARCHIVED_2026-10-08.md). Recover via git history.

## Still optional

- Remaining `p0_batch03_*` / `p0_batch04_*` / `p0_geosite_*` yaml if still present
- Snapshot trees under `config/p0_*_snapshots/` (except batch01)
- Delete stale remote branches `chore/p0-p2-*`
