# Artifact Store migration (Collection volume)

## Problem

Tracked tree ≈ multi-GiB under `data/` + `backup/` (audit ~8.85 GiB). Git is overloaded as identity + artifact + archive store.

## Target split

| Store | Contents |
|-------|----------|
| **Git** | config, policy, scripts, schemas, small manifests, checksums, `rule/` identity, lock files |
| **Artifact Store** | `data/runs/*`, large IR (`rules_v2_full.jsonl`), historical `backup/`, bulky generated snapshots |

Git retains: `run_id`, `artifact_uri`, `sha256`, provenance only.

## Phases

1. **Inventory** — `scripts/size_gate.py` SCAN roots + reports (done, transitional thresholds).
2. **Retention** — weekly dry-run; explicit `--apply` only (`retention.yml`).
3. **External store** — R2/S3/GH release assets; write URI into run manifest.
4. **Stop committing** large paths; CI downloads by digest.
5. **Lower** `max_file_mb` → 5 and `max_tracked_tree_mb` → ~90.

## Do not

- Force-delete `backup/` without retention plan + referenced release preservation.
- Rely on Size Gate alone to shrink history (needs store migration).
