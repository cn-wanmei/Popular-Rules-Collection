# 文档与生产链 SSOT

## 当前生产 SSOT
- `README.md`：生产边界与入口
- `docs/PRODUCTION_RULE_CHAIN.md`：完整生产 DAG
- `docs/GENERATED_OUTPUTS.md`：最终发行目录契约
- `docs/ROUTING_CONTRACT.md` / `docs/ROUTING_DECISION_SSOT.md`：分流决策规范
- `assets/icons/v3/release-pointer.json`：当前 Icon System 3 release
- `generated/manifest.json`：最终文件清单
- `generated/network_manifest.json`：Network Dataset provenance

## 当前 V3 真源
```text
upstream → backup/<collection-date> → data/runs/<run-id>/canonical
→ data/runs/<run-id>/ir → 7 client adapters + Network Dataset
→ Release Candidate → generated/
```

## 目录边界
| 路径 | 当前职责 |
|---|---|
| `data/runs/<run>/canonical/` | V3 Canonical 真源 |
| `data/runs/<run>/ir/` | Semantic IR |
| `generated/<client>/` | 最终客户端规则 |
| `generated/<network-scope>/` | Network Dataset |
| `rule/` | V1 历史浏览/迁移树 |
| `rules/` | V3 目录契约 |
| `database/services/` | Legacy evidence |
| `docs/rules/` | 人类可读派生说明页 |

历史 Phase / V1 / V2 文档仅作记录，不覆盖当前 SSOT。