# Publish & CI status

Repository: https://github.com/cn-wanmei/Popular-Rules-Collection

## Pipeline

**Actions → Collect Upstream → Run workflow**

```
validate_registry → collect → normalize → deduplicate → conflict_detector → provenance
  → build×7 (mihomo / sing-box / surge / shadowrocket / quantumult-x / egern / loon)
  → schema_validate → validate → builder_validate
  → statistics / generate_links / generate_docs (soft)
  → generate_rule_pages --strict → size_gate → commit
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

## Hagezi

Registry collects **Light + Pro + Ultimate**. Profiles (minimal/balanced/full) are a later layer.

## Registry V3

`rules: [{path, name, local?}]` — single place to add services. No `SOURCE_FILES` in code.

**Dead upstream paths** must be removed from registry (not left as permanent fetch failures). Prefer MetaCubeX geosite when BM path 404s.

### BlackMatrix7 dead paths (removed 2026-08-27)

| name | path | reason | coverage |
|------|------|--------|----------|
| taobao | rule/Clash/TaoBao/TaoBao.yaml | HTTP 404 | covered by `alibaba` (BM + MetaCubeX) |
| qq | rule/Clash/QQ/QQ.yaml | HTTP 404 | covered by `tencent` (BM + MetaCubeX) |
| amazonaws | rule/Clash/AmazonAWS/AmazonAWS.yaml | HTTP 404 | covered by `amazon` (BM) + `aws` (MetaCubeX) |
| snapchat | rule/Clash/Snapchat/Snapchat.yaml | HTTP 404 | no alternate upstream — leave unmaterialized |

## Source health visibility

After collect, inspect:

- `sources/health.yaml` — per-source `files_ok` / `files_failed` / `status`
- `backup/<date>/manifests/<source>.json` — per-file `status` / `error` for failed entries

Degraded (`files_failed > 0`) is expected to remain visible in health until the next successful full fetch or registry cleanup.

## Phase 2B-Tier0 (AI / Cloud)

| id | source | status |
|----|--------|--------|
| perplexity | MetaCubeX geosite | registered |
| groq | MetaCubeX geosite | registered (small set) |
| xai | MetaCubeX geosite | registered |
| firebase | MetaCubeX geosite | registered |
| aws | MetaCubeX geosite | registered |
| mistral | — | no upstream yet (primary mapping only) |
| gcp | — | no upstream yet (primary mapping only) |
| supabase | — | no upstream yet (primary mapping only) |
