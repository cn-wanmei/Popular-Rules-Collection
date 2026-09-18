# Pipeline & Publish

## Current production entry points

```bash
python -m src.engine.cli all
python -m src.engine.cli naming_gate
python -m src.engine.cli promote --run-id <id>
python -m src.engine.cli rollback --run-id <id>
```

`make` delegates to the same V3 engine entry point.

## Production flow

```text
upstream collection
  ↓
immutable snapshot
  ↓
ingest / source gate / quarantine
  ↓
canonical
  ↓
hierarchy
  ↓
semantic IR
  ↓
seven native client adapters
  ↓
diff / golden / observability / CAS
  ↓
RC_READY
  ↓
atomic promotion
```

`database/services/` is Legacy Source only. `rule/` is the active V1 Canonical model and is the target of the Phase 1 runtime cutover; until that cutover lands, the V3 production DAG remains acquisition-driven.

## Release control-plane rules

- Release evidence authority is `data/runs/<run-id>/release/manifest.json`.
- The semantic diff baseline is `data/baseline/canonical.json`.
- The operational metrics baseline is `data/baseline/latest.json`.
- Promotion must be `RC_READY` and fail closed on any hard gate.
- Legacy deletion is never automatic.
