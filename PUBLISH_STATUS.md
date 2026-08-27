# Publish & CI status

Repository: https://github.com/cn-wanmei/Popular-Rules-Collection

**Release lock:** [`docs/RELEASE_AND_QC.md`](docs/RELEASE_AND_QC.md)  
**Status:** 可发布/可使用 · 持续 QC（P1-0…P1-3 已落地）

## Pipeline

```
validate_registry → collect → normalize → deduplicate → conflict_detector → provenance
  → build×7 → schema_validate → validate → builder_validate
  → identity_validate (soft) → rule_count_drift (soft)
  → statistics / docs (soft) → generate_rule_pages --strict → size_gate
  → commit → git pull --rebase origin main → push
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

## Source health & drift

- `sources/health.yaml` — never hide `files_failed`
- Dead paths: **explicit** registry fix only (no Collector fuzzy match)
- Soft QC: identity NAME check, rule-count delta, domain quality width

## Intentional unmaterialized

SSOT: `config/intentional_unmaterialized.yaml`  
mistral / gcp / supabase / roblox / minecraft — `no_verified_upstream`  
blizzard → `maps_to_battlenet` · stripe · adblock-light/pro (deferred)

## Gaming

- **garena** — BM registered  
- **roblox / minecraft** — no verified BM/MetaCubeX path as of 2026-08-27  

## Phase 3

- **3A/3B** — release_snapshot / generated_manifest / source_snapshot / service_score + intentional SSOT ✅  
- **3C next batch** — anthropic, digitalocean, atlassian, slack, line, kakaotalk, adobe, oracle (verified BM)  
  → `reports/candidates/batch_3c_2026-08-27.md`  
