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
