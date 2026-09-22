# DeepSeek

> Current V3 service documentation. Subscription paths are derived from `generated/manifest.json`.

| 项目 | 内容 |
|------|------|
| Rule ID | `deepseek` |
| Primary Ecosystem | `deepseek` |
| Service Type | service |
| Parent Aggregate | — |
| Release Date | 2026-09-22 |
| Dedicated client outputs | 7 / 7 |

## 当前生产订阅路径

| 客户端 | 路径 | Raw |
|--------|------|-----|
| egern | `egern/deepseek/deepseek/rules.yaml` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/egern/deepseek/deepseek/rules.yaml) |
| loon | `loon/deepseek/deepseek/rules.list` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/loon/deepseek/deepseek/rules.list) |
| mihomo | `mihomo/deepseek/deepseek/rules.yaml` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/mihomo/deepseek/deepseek/rules.yaml) |
| quantumultx | `quantumultx/deepseek/deepseek/rules.list` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/quantumultx/deepseek/deepseek/rules.list) |
| shadowrocket | `shadowrocket/deepseek/deepseek/rules.list` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/shadowrocket/deepseek/deepseek/rules.list) |
| singbox | `singbox/deepseek/deepseek/rules.json` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/singbox/deepseek/deepseek/rules.json) |
| surge | `surge/deepseek/deepseek/rules.list` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/surge/deepseek/deepseek/rules.list) |

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
