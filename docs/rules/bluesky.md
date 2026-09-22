# Bluesky

> Current V3 service documentation. Subscription paths are derived from `generated/manifest.json`.

| 项目 | 内容 |
|------|------|
| Rule ID | `bluesky` |
| Primary Ecosystem | `bluesky` |
| Service Type | service |
| Parent Aggregate | — |
| Release Date | 2026-09-22 |
| Dedicated client outputs | 7 / 7 |

## 当前生产订阅路径

| 客户端 | 路径 | Raw |
|--------|------|-----|
| egern | `egern/bluesky/bluesky/rules.yaml` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/egern/bluesky/bluesky/rules.yaml) |
| loon | `loon/bluesky/bluesky/rules.list` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/loon/bluesky/bluesky/rules.list) |
| mihomo | `mihomo/bluesky/bluesky/rules.yaml` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/mihomo/bluesky/bluesky/rules.yaml) |
| quantumultx | `quantumultx/bluesky/bluesky/rules.list` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/quantumultx/bluesky/bluesky/rules.list) |
| shadowrocket | `shadowrocket/bluesky/bluesky/rules.list` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/shadowrocket/bluesky/bluesky/rules.list) |
| singbox | `singbox/bluesky/bluesky/rules.json` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/singbox/bluesky/bluesky/rules.json) |
| surge | `surge/bluesky/bluesky/rules.list` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/surge/bluesky/bluesky/rules.list) |

## 当前真源边界

- V3 Canonical：`data/runs/<run-id>/canonical/`
- Semantic IR：`data/runs/<run-id>/ir/`
- 最终发行：`generated/`
- `rule/`：V1 历史浏览/迁移树
- `rules/`：V3 目录契约
- `database/services/`：Legacy evidence，不是 V3 Runtime 真源

## 目录契约

当前客户端目录只能使用 `mihomo`、`singbox`、`surge`、`shadowrocket`、`quantumultx`、`egern`、`loon`。历史 `sing-box` / `quantumult-x` 名称不属于当前目录契约。

---
_页面日期来源：2026-09-22。生产路径来源：generated/manifest.json。_
