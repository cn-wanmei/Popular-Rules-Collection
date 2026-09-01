# Engine v3 Independent Kernel (1.0.1)

## Status

- Product version: `1.0.1`
- Engine codename: `v3` (metadata only)
- **V2 Runtime Dependency: 0**

## Hard guarantees

1. No runtime read of `database/services` after Snapshot.
2. Pipeline order is fixed and enforced:
   ```
   snapshot → ingest → quarantine → canonical
   → hierarchy → ir → adapters → diff → golden → release
   ```
3. Publish / Promote only when Release State == `RC_READY`.
4. All build artifacts live under `data/runs/<run_id>/` first (atomic).
5. Native client formats (correct extensions).
6. Full hierarchy + decisions inside IR.
7. True reproducibility digests + compare.

## CLI

```bash
# Full pipeline
python -m src.engine.cli all --sources ./sources --data ./data

# Migrate legacy database/services → Snapshot (one-time / bridge)
python -m src.engine.cli migrate-legacy --database-services ./database/services

# Promote RC_READY run into generated/
python -m src.engine.cli promote --run-id <run_id>

# Rollback
python -m src.engine.cli rollback --run-id <previous_run_id>

# Reproducibility
python -m src.engine.cli reproducibility --run-a data/runs/A --run-b data/runs/B
python -m src.engine.cli digest --run data/runs/<run_id>
```

## Migration path

```
database/services/*.yaml
        ↓  (migrate-legacy only)
data/snapshots/<snapshot_id>/sources/services/
        ↓
Engine Ingest → Quarantine → Canonical → … → Release
```

After the first successful Snapshot, the Engine never opens `database/services` again.

## Directory contract

```
data/
├── snapshots/<snapshot_id>/
│   ├── manifest.json
│   └── sources/
├── runs/<run_id>/
│   ├── canonical/
│   ├── hierarchy/
│   ├── ir/
│   ├── artifacts/{mihomo,singbox,...}/
│   ├── quarantine/
│   ├── reports/diff/
│   ├── golden/
│   ├── release/
│   ├── reproducibility/
│   └── run_manifest.json
└── generated/          # only after promote
```

## Acceptance

| Gate | Requirement |
|------|-------------|
| V2 Runtime Dependency | 0 |
| Snapshot-first | yes |
| Quarantine-first | yes |
| Canonical silent-drop | forbidden |
| Native adapters | correct extensions |
| Hierarchy in IR | full |
| Decision deterministic | yes |
| Golden L1–L7 | real checks |
| Release before Publish | yes |
| Reproducibility | hash compare |
| Rollback | tested |
