# Booking

> Current V3 service documentation. Subscription paths are derived from `generated/manifest.json`.

| 项目 | 内容 |
|------|------|
| Rule ID | `booking` |
| Primary Ecosystem | `booking` |
| Service Type | service |
| Parent Aggregate | — |
| Release Date | 2026-09-22 |
| Dedicated client outputs | 7 / 7 |

## 当前生产订阅路径

| 客户端 | 路径 | Raw |
|--------|------|-----|
| egern | `egern/booking/booking/rules.yaml` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/egern/booking/booking/rules.yaml) |
| loon | `loon/booking/booking/rules.list` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/loon/booking/booking/rules.list) |
| mihomo | `mihomo/booking/booking/rules.yaml` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/mihomo/booking/booking/rules.yaml) |
| quantumultx | `quantumultx/booking/booking/rules.list` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/quantumultx/booking/booking/rules.list) |
| shadowrocket | `shadowrocket/booking/booking/rules.list` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/shadowrocket/booking/booking/rules.list) |
| singbox | `singbox/booking/booking/rules.json` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/singbox/booking/booking/rules.json) |
| surge | `surge/booking/booking/rules.list` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/surge/booking/booking/rules.list) |

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
