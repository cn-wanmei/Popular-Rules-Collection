# Process artifact archive inventory

## CI-held — KEEP

| Asset | Consumer |
|-------|----------|
| `scripts/phase_j_p0_service_evidence.py` | `build.yml` |
| `config/p0_materialization.yaml` | phase_j |
| `config/p0_service_identity.yaml` | phase_j |
| `scripts/p0_batch01_semantic_overlap_audit.py` | `publish.yml` |
| `config/p0_batch01_*` + snapshots | batch01 |
| **`config/p0_batch02_*`** | repository tests / evidence gate |
| **`config/p0_batch03_*`** | repository tests / evidence gate (28 services) |
| **`config/v1_final_migration_gate.yaml`** | Phase 8 + unit tests |
| `scripts/legacy_*.py` / `database/` | until Phase 8 PASS |

## Deferred (do not delete until local `pytest` + `rg` pass)

| Asset | Reason |
|-------|--------|
| `config/p0_batch04_*` + `p0_batch04_snapshots/` | Process batch; no hard CI path found in phase_j/batch01 scripts, but **do not archive without full-repo grep + Unit Tests green** (2026-10-08 incident) |
| `config/p0_geosite_*` + snapshots | Large process artifacts; same gate |
| `config/p0_source_bridge_*` | Bridge process |
| `config/p0_source_snapshots/` (non-batch01) | Shared by batch evidence paths — treat as KEEP until proven unused |

## Ops 2026-10-08

- CI restored: Unit Tests + Engine v3 **success** @ `77e77de9`
- Stale branches `chore/p0-p2-*` deleted
- Collect Upstream dispatched (refresh degraded health)
- Retention workflow dispatched (dry-run schedule path)

## Incident note

Premature archive of CI-held configs caused multi-run failures. Prefer soft-move only after KEEP table update + CI green.
