# Perplexity

> Current V3 service documentation. Subscription paths are derived from `generated/manifest.json`.

| 项目 | 内容 |
|------|------|
| Rule ID | `perplexity` |
| Primary Ecosystem | `perplexity` |
| Service Type | service |
| Parent Aggregate | — |
| Release Date | 2026-09-22 |
| Dedicated client outputs | 7 / 7 |

## 当前生产订阅路径

| 客户端 | 路径 | Raw |
|--------|------|-----|
| egern | `egern/perplexity/perplexity/rules.yaml` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/egern/perplexity/perplexity/rules.yaml) |
| loon | `loon/perplexity/perplexity/rules.list` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/loon/perplexity/perplexity/rules.list) |
| mihomo | `mihomo/perplexity/perplexity/rules.yaml` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/mihomo/perplexity/perplexity/rules.yaml) |
| quantumultx | `quantumultx/perplexity/perplexity/rules.list` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/quantumultx/perplexity/perplexity/rules.list) |
| shadowrocket | `shadowrocket/perplexity/perplexity/rules.list` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/shadowrocket/perplexity/perplexity/rules.list) |
| singbox | `singbox/perplexity/perplexity/rules.json` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/singbox/perplexity/perplexity/rules.json) |
| surge | `surge/perplexity/perplexity/rules.list` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/surge/perplexity/perplexity/rules.list) |

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
