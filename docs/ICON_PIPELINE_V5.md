# Icon Pipeline V5 — Production Architecture

**SSOT variants (8):** `source_original`, `glassmorphism`, `soft_3d`, `neo_skeuomorphism`, `minimalist`, `duotone_line`, `mbe`, `y2k`

## Modes

| Mode | Timeout | Baseline | Shards | Promote |
|------|--------:|----------|--------|---------|
| `incremental` (default) | 30m | rsync production → build | no | opt-in PR |
| `full` | 40m × N shards + merge | cold / refresh | `hash(service_id)%N` | opt-in PR after ≥90% |

## Phase status

| Phase | Status | Deliverables |
|------:|--------|--------------|
| 1 | done | baseline, mode SLA, Actions cache, promote opt-in |
| 2 | done | `assets/icon-source-cache/`, entry `source_hash` + `renderer_version` invalidation |
| 3 | done | `shard-plan` / matrix full build / `merge-shards` / coverage gate ≥90% |
| 4 | done | `build-manifest.json`, CAS `objects/sha256/`, `failures.json` queue |

## CLI

```bash
python scripts/icon_system_v5.py build --incremental --concurrency 16 ...
python scripts/icon_system_v5.py build --shard-index 0 --shard-count 4 ...
python scripts/icon_system_v5.py shard-plan --shards 4 --out build/matrix.json
python scripts/icon_system_v5.py merge-shards --registries-glob 'shards/**/registry.json' --out build/icon-v5/registry.json
python scripts/icon_system_v5.py write-manifest --registry ... --out build-manifest.json
```

## Rules

1. Never write production from runner except via promote PR.
2. Partial artifacts allowed; production requires coverage gate.
3. Coverage = dynamic rule-index services × 8/8.
