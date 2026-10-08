# Provenance classification (394 Collection services)

Goal: **394/394 explicit provenance class**, not necessarily 394 Source durable.

## Classes

| Class | Meaning |
|-------|---------|
| `source_durable` | Immutable Source seal + Collection binding |
| `upstream_managed` | Active upstream (blackmatrix7 / metacubex / v2fly / dler / …) |
| `legacy_upstream` | Upstream path retained, migration pending |
| `self_built_verified` | Source self-built + verified evidence |
| `self_built_review` | Self-built still in REVIEW |
| `intentional_unmaterialized` | Policy: no materialization |
| `retired` | Explicitly retired |
| `non_routable` | Identity only / no routing artifact |

## Current scale (audit 2026-10-08)

- Collection `entity:service` ≈ 394
- Source services ≈ 282
- Intersection ≈ 280 → remaining Collection services need class assignment (mostly upstream_managed)

## Process

1. Never bulk-delete Collection services to “match” Source count.
2. Classify via `config/` + immutable registry, not README prose.
3. Track Source-only (`baidu`, etc.) as Identity Accept candidates separately.
