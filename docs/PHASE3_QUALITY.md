# Phase 3A — Dataset Quality Gate

## Tiers

| Tier | Examples | CI |
|------|----------|-----|
| **Hard Fail** | empty required dataset, syntax failure, shrink ≥90%, generated missing, disappeared large dataset, mmdb size mismatch | exit 1 |
| **Warning** | shrink 30–90%, growth ≥300%, source degraded/blocked, soft provenance gaps | continue (unless `--strict`) |
| **Informational** | normal ok counts, new dataset, stable sha | log only |

## Scripts

```text
dataset_diff.py      → reports/<date>/dataset_diff.json
                     → reports/<date>/dataset_snapshot.json
                     → reports/dataset_baseline.json
dataset_quality.py   → reports/<date>/dataset_quality.json
```

Diff fields: `old_count`, `new_count`, `added`, `removed`, `shrink_ratio`, `growth_ratio`, `sha_changed`.

## Health layers

```text
Source Health → Collection → Dataset Health → Build Health → Release Health
```

Single upstream 404 must not fail the pipeline if the dataset still materializes.

## Non-goals (3A)

- No Builder / Primary changes
- No bulk new Services
- No Coverage Matrix UI (Phase 3B)
