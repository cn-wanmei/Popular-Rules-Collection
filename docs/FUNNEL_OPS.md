# Source → Collection funnel operations

Companion to [`SOURCE_COLLECTION_FUNNEL.md`](SOURCE_COLLECTION_FUNNEL.md).

## Source health (Collection view)

Derived from telemetry + `config/health_policy.yaml`:

| Class | Meaning |
|-------|--------|
| `healthy` | age ≤ 48h |
| `degraded` | age ≤ 168h (7d) |
| `failed` | failure_count > 0 or unknown policy |

`PUBLISH_STATUS.md` reports counts only. For names:

```bash
# Collection
python scripts/classify_health.py   # or inspect sources/health.yaml if present

# Source repo
python -m source_engine health
python -m source_engine gap --service <id>
```

Occasional upstream 404 is **not** project failure (see RELEASE_AND_QC).

## Weekly canary quota

- Target: ≥ **8** services `VERIFIED → CANARY` per week (Source lifecycle).
- No skip levels; Collection production still requires immutable binding.
- Batch reason example: `weekly_funnel_quota_YYYY-MM-DD`.

## Priority for acceleration

1. `BLOCKED` / `domains=0` → fix or tombstone
2. Long-lived `REVIEW` with official evidence → `qualify` → `VERIFIED`
3. `VERIFIED` with high domain count / P0 product → CANARY batch
4. CANARY with Collection handoff seal → Collection canary → production

## Degraded response playbook

When `degraded` count rises:

1. List degraded source ids from health classifier.
2. Re-fetch / repair on Source (`source_engine repair`).
3. If upstream permanently gone → intentional unmaterialized or BLOCKED + funnel note.
4. Do not clear LKG with empty fetch results.
