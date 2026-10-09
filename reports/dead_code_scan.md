# Dead code / redundant config scan

**Generated:** 2026-10-09 (audit follow-up)  
**Scope:** `Popular-Rules-Collection` scripts + config references  
**Method:** Cross-reference `scripts/*` against `.github/workflows/*`, `scripts/SCRIPTS_INDEX.md`, `config/builder_registry.yaml`, `config/ci_gates.yaml`

## Summary

| Class | Count | Action |
|-------|------:|--------|
| Scripts referenced by workflows / index | 61 | Keep |
| Historical one-off phase / v1 / migrate tools | 21 | **Moved** → `scripts/archive/historical/` |
| Other scripts not in workflows/index | 39 | Retain pending engine/import graph audit |
| Config already archived | `config/archive/icon-v5/` | No change |
| Stale docs marked historical (prior PR) | HOT_MISSING, completion-reconciliation, SERVICE_CATALOG, FUNNEL_TRIAGE | Done |

## Archived in this change (21)

Moved from `scripts/` → `scripts/archive/historical/`:

- `archive_phase_candidates.sh`
- `legacy_delete.py`
- `migrate_directory_layout_v2.py`
- `p0_batch01_semantic_overlap_report.py`
- `p2_baseline_freeze.py`
- `phase2_service_identity_reconciliation.py`
- `phase_a_current_health.py` … `phase_o_r_operational_closure.py` (phase_* suite)
- `v1_final_migration_gate.py`, `v1_phase2_8_integrity.py`, `v1_phase2_audit.py`

Rationale: one-shot migration / phase gates; **not** invoked by any active workflow; names encode completed phases (A–O, v1).

## Retain for follow-up (not moved)

These appear unused by workflows but may be invoked by engine builders, local ops, or docs:

`attach_artifact_provenance.py`, `build_artifact_manifest.py`, `build_network_datasets.py`, `build_network_lan.py`, `build_provider_datasets.py`, `build_resolution_fragment.py`, `build_routing_policies.py`, `builder_validate.py`, `collect_datasets.py`, `collect_ip.py`, `collect_providers.py`, `diff_report.py`, `gate_failure_injection.py`, `generate_links.py`, `generate_readme.py`, `git_skip_release_paths.py`, `growth_anomaly.py`, `hierarchy_*`, `icon_resolver_v6.py`, `ip_cidr.py`, `ip_quality_audit.py`, `pack_release_artifacts.py`, `profile_validate.py`, `promote_baseline.py`, `release_snapshot.py`, `resolve_hierarchy.py`, `routing_*`, `rule_count_drift.py`, `run_gated.py`, `semantic_dedup.py`, `service_score.py`, `source_quarantine.py`, `source_snapshot.py`, `validate_dataset_registry.py`, `validate_registry.py`

**Next scan:** import graph from `src/engine/` + `config/builder_registry.yaml` entrypoints before any further moves.

## Config notes

- `config/archive/icon-v5/` — already isolated; do not load in V6 paths.
- `config/p0_batch0*_snapshots/` — evidence snapshots for P0 audits; keep as historical evidence (not runtime).
- Prefer `SERVICE_CATALOG.generated.md` over hand-maintained `SERVICE_CATALOG.md` (banner applied).

## Case-path note

`docs/architecture.md` is a compatibility stub; canonical doc is `docs/ARCHITECTURE.md`.
