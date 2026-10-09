# Scripts index (domain orientation)

## CI / gates
- `architecture_gate.py`, `quality_validate.py`, `identity_validate.py`
- `check_icon_pointers.py`, `entity_coverage_report.py`
- `publish_fail_closed_gate.py`, `immutable_source_lineage_gate.py`

## Build / collect
- `collect.py`, `build_*.py`, `build_universal_ir.py`

## P0 production evidence (**KEEP** — used by CI)
- `phase_j_p0_service_evidence.py` — `build.yml`
- `p0_batch01_semantic_overlap_audit.py` — `publish.yml`
- `p0_service_production_gate.py`

## Retention
- `retention.py` + `.github/workflows/retention.yml`

## Legacy (**KEEP** until Phase 8 PASS)
- `legacy_*.py`


## Archive / historical (2026-10-09)

Phase-completion and v1 migration tools live under [`scripts/archive/historical/`](archive/historical/).
They are not CI entrypoints. Full scan: [`reports/dead_code_scan.md`](../reports/dead_code_scan.md).

### Round 2 import graph

12 more scripts archived (no engine/CI refs or docs-only). Details: [`reports/dead_code_scan.md`](../reports/dead_code_scan.md).
