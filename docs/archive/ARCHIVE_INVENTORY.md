# Process artifact archive inventory

## CI-held — KEEP

| Asset | Consumer |
|-------|----------|
| `scripts/phase_j_p0_service_evidence.py` | `build.yml` |
| `config/p0_materialization.yaml` | phase_j |
| `config/p0_service_identity.yaml` | phase_j |
| `scripts/p0_batch01_semantic_overlap_audit.py` | `publish.yml` |
| `config/p0_batch01_*` + snapshots | batch01 |
| **`config/p0_batch02_*`** (membership/semantic/overlap/source_evidence) | repository tests / evidence gate |
| **`config/p0_batch03_*`** (membership/semantic/overlap/source_evidence) | repository tests / evidence gate (28 services) |
| **`config/v1_final_migration_gate.yaml`** | `tests/engine/test_v1_final_migration_gate.py` + Phase 8 |
| `scripts/legacy_*.py` / `database/` | until Phase 8 PASS |

## Incident 2026-10-08

Premature archive of `v1_final_migration_gate` + batch02/03 caused Unit Tests + Engine failures.
Restored on main: `921a6535` (gate), `bc29c93a` (overlap), `77e77de9` (membership/semantic/source_evidence).

## Optional later

- batch04 / geosite process yaml only after confirming no test/script readers
- Snapshot trees except batch01
- Delete stale remote branches `chore/p0-p2-*`
