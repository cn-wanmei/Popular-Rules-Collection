# Icon Pipeline V5 — Production Architecture (Phase 1)

**SSOT styles (8 only):** `source_original`, `glassmorphism`, `soft_3d`, `neo_skeuomorphism`, `minimalist`, `duotone_line`, `mbe`, `y2k`

## Modes

| Mode | Timeout | Baseline | Incremental | Refresh |
|------|--------:|----------|-------------|---------|
| `incremental` (default) | 30 min | rsync `assets/icons/v5` → `build/icon-v5` | yes | no |
| `full` | 120 min | skip | no | yes |

## Rules

1. Production tree is **not** a runner scratchpad — write via artifact → PR → merge only.
2. Partial acquisition artifacts are allowed; **promote remains opt-in** and gated (≥90% complete_8_of_8).
3. Coverage is **dynamic rule-index × 8/8**, never a fixed 146.

## Phase roadmap

- Phase 1 (this): baseline, mode SLA, Actions cache, metrics JSON
- Phase 2: richer source cache + registry source_hash/renderer_version driven invalidation
- Phase 3: matrix shards (`hash(service_id)%N`) + merge
- Phase 4: manifest + CAS + failed queue
