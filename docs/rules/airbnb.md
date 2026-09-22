# Airbnb

> Current V3 service documentation. Subscription paths are derived from `generated/manifest.json`; this page is not a rule database.

| 项目 | 内容 |
|------|------|
| Rule ID | `airbnb` |
| Primary Ecosystem | `airbnb` |
| Service Type | service |
| Parent Aggregate | — |
| Release Date | 2026-09-22 |
| Dedicated client outputs | 7 / 7 |

## 当前生产订阅路径

| 客户端 | 路径 | Raw |
|--------|------|-----|
| egern | `egern/airbnb/airbnb/rules.yaml` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/egern/airbnb/airbnb/rules.yaml) |
| loon | `loon/airbnb/airbnb/rules.list` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/loon/airbnb/airbnb/rules.list) |
| mihomo | `mihomo/airbnb/airbnb/rules.yaml` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/mihomo/airbnb/airbnb/rules.yaml) |
| quantumultx | `quantumultx/airbnb/airbnb/rules.list` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/quantumultx/airbnb/airbnb/rules.list) |
| shadowrocket | `shadowrocket/airbnb/airbnb/rules.list` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/shadowrocket/airbnb/airbnb/rules.list) |
| singbox | `singbox/airbnb/airbnb/rules.json` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/singbox/airbnb/airbnb/rules.json) |
| surge | `surge/airbnb/airbnb/rules.list` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/surge/airbnb/airbnb/rules.list) |

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
