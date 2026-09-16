# Publish & CI status

Repository: https://github.com/cn-wanmei/Popular-Rules-Collection

**Release lock:** [`docs/RELEASE_AND_QC.md`](docs/RELEASE_AND_QC.md)  
**Status:** 当前发布链路按 V3 Engine 运行；Collection、Build、Publish 均受 CI Gate 控制。若最新工作流失败，应以 GitHub Actions 实际运行结果为准。

## V3 Pipeline

```
validate_registry / validate_dataset_registry / validate_ip_registry
  → collect / collection DAG
  → immutable snapshot
  → ingest → quarantine → canonical
  → hierarchy / decision → IR
  → adapters ×7
  → diff → golden → release gate
  → atomic promotion → generated/
```

网络数据链路与 Service Rules 分离：

```
collect_datasets / collect_ip / collect_providers
  → database/{network,geosite,geoip,provider,asn,policies}
  → dataset validation
  → generated/{network,geosite,geoip,provider,mmdb}
```

**V3 Build entry:** `PYTHONPATH=. python -m src.engine.cli all`  
**V3 Publish entry:** `PYTHONPATH=. python -m src.engine.cli promote --run-id <run_id>`

旧版 `scripts/normalize.py`、`scripts/deduplicate.py` 与旧 `scripts/build_*.py` 已退出生产链，仅作为迁移阶段遗留工具保留。

## Clients (7)

| Client | Output |
|--------|--------|
| Mihomo | `generated/mihomo/{id}.yaml` |
| sing-box | `generated/singbox/{id}.json` |
| Surge | `generated/surge/{id}.list` |
| Shadowrocket | `generated/shadowrocket/{id}.list` |
| Quantumult X | `generated/quantumultx/{id}.list` |
| Egern | `generated/egern/{id}.yaml` |
| Loon | `generated/loon/{id}.list` |

目录名称以 `config/builder_registry.yaml` / `config/formats.yaml` 为准。

## Source health & drift

- `sources/health.yaml` — 永不隐藏 `files_failed`
- Dead paths: **explicit** registry fix only (no Collector fuzzy match)
- Soft QC: identity NAME check, rule-count delta, domain quality width
- Collection manifest 必须与本轮固定 `collection_date` 一致

## Intentional unmaterialized

SSOT: `config/intentional_unmaterialized.yaml`  
mistral / gcp / supabase / roblox / minecraft — `no_verified_upstream`  
blizzard → `maps_to_battlenet` · stripe · adblock-light/pro（deferred）

taobao / qq / baidumap / baidupan / quickpass / googledrive / googlemaps / temu / jdfinance / amazonaws / dingtalk / siri / steamcn 等按该 SSOT 的 aggregate / mapping 规则处理。

## Gaming

- **garena** — BM registered
- **roblox / minecraft** — no verified BM/MetaCubeX path as of 2026-08-27

## Phase 3

- **3A/3B** — release_snapshot / generated_manifest / source_snapshot / service_score + intentional SSOT ✅
- **3C next batch** — anthropic, digitalocean, atlassian, slack, line, kakaotalk, adobe, oracle（verified BM）
  → `reports/candidates/batch_3c_2026-08-27.md`

## Operational note

历史快照是否继续保留由后续 retention policy 决定；不要以单次 CI 失败直接判断已发布规则失效。当前状态以 GitHub Actions 与最近一次成功 Collection / Build / Publish 为准。
