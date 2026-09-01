# Architecture (1.1)

- **Product version:** 1.0.x (`VERSION`)
- **Engine:** `src/engine/` is the sole service-rule build/runtime path.
- **Input boundary:** upstream collection lands in `backup/<date>/` and is frozen into an immutable Snapshot.
- **Workspace:** `data/runs/<run_id>/` contains immutable build outputs and release evidence.
- **Public tree:** `generated/` is the published projection only; it is never an input SSOT.
- **Legacy:** `scripts/normalize.py`, `scripts/deduplicate.py`, and `scripts/build_*.py` are deprecated and are not production pipeline stages.

```text
sources / upstream collection
          ↓
     immutable snapshot
          ↓
        ingest
          ↓
      quarantine
          ↓
       canonical
          ↓
   hierarchy + decision
          ↓
           IR
          ↓
    7 client adapters
          ↓
        diff
          ↓
       golden
          ↓
     release gate
          ↓
   atomic promotion
          ↓
      generated/
```

## Production boundary

`collect.py` and the dataset collectors are transport/fetch steps only. Service-rule normalization and multi-client build happen inside `src/engine/`.

`database/services` is not a V3 runtime input. Legacy data can only enter through `src/engine/ingest/migrate_legacy.py` as a one-time migration bridge.
