# Publish & CI status

Repository: https://github.com/cn-wanmei/Popular-Rules-Collection

**Release lock:** see [`docs/RELEASE_AND_QC.md`](docs/RELEASE_AND_QC.md)  
**Status:** 规则生成可发布/可使用；治理进入持续 QC（Phase 2B P1）。

## Pipeline

**Actions → Collect Upstream → Run workflow**

```
validate_registry → collect → normalize → deduplicate → conflict_detector → provenance
  → build×7 (mihomo / sing-box / surge / shadowrocket / quantumult-x / egern / loon)
  → schema_validate → validate → builder_validate
  → statistics / generate_links / generate_docs (soft)
  → generate_rule_pages --strict → size_gate → commit
  → git pull --rebase origin main → git push
```

Hard gates: `validate_registry`, `schema_validate`, `validate`, `builder_validate`, `generate_rule_pages`, `size_gate`.

## Clients (7)

| Client | Output |
|--------|--------|
| Mihomo | `generated/mihomo/{id}.yaml` |
| sing-box | `generated/sing-box/{id}.json` |
| Surge | `generated/surge/{id}.list` |
| Shadowrocket | `generated/shadowrocket/{id}.list` |
| Quantumult X | `generated/quantumult-x/{id}.list` |
| Egern | `generated/egern/{id}.yaml` |
| Loon | `generated/loon/{id}.list` |

## Source health

After collect, inspect:

- `sources/health.yaml` — `files_ok` / `files_failed` / `status` / `last_success`
- `backup/<date>/manifests/<source>.json` — per-file errors

Degraded remains visible until the next successful full fetch or explicit registry cleanup.  
**Do not** hide `files_failed` to force “100% health.”

### Registry drift policy

Dead upstream paths must be **removed or rewritten explicitly** in `sources/registry.yaml`.  
Collector must **not** fuzzy-match paths. Prefer alternate verified upstream (e.g. MetaCubeX) when BM 404s.

### BlackMatrix7 path notes (2026-08-27)

| name | resolution |
|------|------------|
| taobao / qq / amazonaws / snapchat | removed dead BM paths; cover via parent/alt where available |
| jingdong | `rule/Clash/JingDong/JingDong.yaml` |
| iqiyi | `rule/Clash/iQIYI/iQIYI.yaml` |

## Intentional unmaterialized

| id | reason |
|----|--------|
| mistral / gcp / supabase | no_verified_upstream (primary only) |
| blizzard | maps to battlenet upstream |

## Phase 2B QC P1

1. **P1-0** Rule schema test — `schema_validate` on `database/services/*.yaml`
2. **P1-1** Source → Service identity
3. **P1-2** Rule count drift (warn-first)
4. **P1-3** Abnormal width / quality (warn-first)

KPI: coverage + source health + builder coverage + validation — **not** “max rule lines.”
