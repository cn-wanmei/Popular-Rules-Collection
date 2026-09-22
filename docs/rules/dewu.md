# Dewu

> Current V3 service documentation. Subscription paths are derived from `generated/manifest.json`.

| 项目 | 内容 |
|------|------|
| Rule ID | `dewu` |
| Primary Ecosystem | `dewu` |
| Service Type | service |
| Parent Aggregate | — |
| Release Date | 2026-09-22 |
| Dedicated client outputs | 7 / 7 |

## 当前生产订阅路径

| 客户端 | 路径 | Raw |
|--------|------|-----|
| egern | `egern/dewu/dewu/rules.yaml` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/egern/dewu/dewu/rules.yaml) |
| loon | `loon/dewu/dewu/rules.list` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/loon/dewu/dewu/rules.list) |
| mihomo | `mihomo/dewu/dewu/rules.yaml` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/mihomo/dewu/dewu/rules.yaml) |
| quantumultx | `quantumultx/dewu/dewu/rules.list` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/quantumultx/dewu/dewu/rules.list) |
| shadowrocket | `shadowrocket/dewu/dewu/rules.list` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/shadowrocket/dewu/dewu/rules.list) |
| singbox | `singbox/dewu/dewu/rules.json` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/singbox/dewu/dewu/rules.json) |
| surge | `surge/dewu/dewu/rules.list` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/surge/dewu/dewu/rules.list) |

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
