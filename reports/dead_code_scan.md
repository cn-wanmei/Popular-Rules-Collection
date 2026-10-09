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


## Round 2 — src/engine import graph (2026-10-09)

Scanned `src/`, `scripts/`, `tests/`, `config/`, `docs/`, `.github/workflows/` (1998 files).

### Classification of prior 39 candidates

| Class | Count | Action |
|-------|------:|--------|
| Referenced by `src/engine`, workflows, or `config/ci_gates.yaml` | 17 | **Keep** in `scripts/` |
| Referenced by tests or peer scripts only | 9 | **Keep** (test/ops graph) |
| Docs-only mentions | 4 | **Archive** this round |
| No external references | 8 | **Archive** this round |

### Keep (engine / CI / config) — 17

`builder_validate.py`, `collect_datasets.py`, `collect_ip.py`, `collect_providers.py`, `generate_links.py`, `growth_anomaly.py`, `ip_cidr.py`, `pack_release_artifacts.py`, `profile_validate.py`, `promote_baseline.py`, `release_snapshot.py`, `routing_emit.py`, `semantic_dedup.py`, `service_score.py`, `source_quarantine.py`, `validate_dataset_registry.py`, `validate_registry.py`

Notable: `ip_cidr.py` is imported across `src/engine` (adapters, ingest, validation). Collect helpers are used from `src/engine/collection/run.py`.

### Keep (tests / peer scripts) — 9

`build_network_datasets.py`, `gate_failure_injection.py`, `hierarchy_coverage.py`, `hierarchy_golden.py`, `hierarchy_validate.py`, `icon_resolver_v6.py`, `resolve_hierarchy.py`, `rule_count_drift.py`, `source_snapshot.py`

### Archived this round — 12

Moved to `scripts/archive/historical/`:

**No external refs (8):**
`build_artifact_manifest.py`, `build_resolution_fragment.py`, `build_routing_policies.py`, `diff_report.py`, `generate_readme.py`, `git_skip_release_paths.py`, `ip_quality_audit.py`, `run_gated.py`

**Docs-only (4):**
`attach_artifact_provenance.py`, `build_network_lan.py`, `build_provider_datasets.py`, `routing_resolve.py`

### Totals after round 2

- Round 1 archived: 21
- Round 2 archived: 12
- **Total archived: 33**
- Remaining active-ish under `scripts/` root: ~87 (CI + engine + tests graph)
