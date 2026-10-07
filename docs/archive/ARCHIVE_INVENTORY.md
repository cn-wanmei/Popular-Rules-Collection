# Process artifact archive inventory

## CI-held — KEEP (do not move)

| Asset | Consumer |
|-------|----------|
| `scripts/phase_j_p0_service_evidence.py` | `build.yml` |
| `config/p0_materialization.yaml` | phase_j |
| `config/p0_service_identity.yaml` | phase_j |
| `scripts/p0_batch01_semantic_overlap_audit.py` | `publish.yml` |
| `config/p0_batch01_semantic_audit.yaml` | batch01 |
| `config/p0_batch01_overlap_audit.yaml` | batch01 |
| `config/p0_batch01_snapshots/**` | batch01 |
| `scripts/legacy_*.py` / `database/` | until Phase 8 PASS |

## Optional physical move

```bash
bash scripts/archive_phase_candidates.sh
# then: verify, commit, push
```

## Landed on main (2026-10-07)

- [x] Root stubs removed (#294)
- [x] KEEP map + inventory
- [x] `retention.yml` weekly dry-run
- [x] `entity_coverage_report.py`
- [x] `FUNNEL_DASHBOARD.md`
- [x] Optional archive runner script
