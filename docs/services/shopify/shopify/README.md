<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/shopify.png" alt="Shopify 图标" width="72" height="72">

# Shopify — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `shopify` |
| 类型 | service |
| Provider | `shopify` |
| 语义规则数量 | **8** |
| 语义 SHA-256 | `78a2a22b2f64cff64c9f3b6565cfb4bd6b8169b9ef58549c74e681e29404a21b` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.shopify`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/shopify.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/shopify/shopify/shopify.yaml` | 16 | 339 | `02b4fcf569eb0f78f927e2949a023bcd333c5d5a38b9da95dabdfb51c42de253` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/shopify/shopify/shopify.yaml) |
| loon | `loon/shopify/shopify/shopify.list` | 16 | 448 | `a6649d50d571b65a5be41d294f1bc0036f60f39b3cdd79f010376faeff2433bc` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/shopify/shopify/shopify.list) |
| mihomo | `mihomo/shopify/shopify/shopify.yaml` | 16 | 521 | `6fd1581fa9f1a9c2f5b7852c3e58834f130651e842475f44f2eb62be5501dadf` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/shopify/shopify/shopify.yaml) |
| quantumultx | `quantumultx/shopify/shopify/shopify.list` | 16 | 544 | `0724f2b7d8885102e46ab6a4597dac5738ab2d265c2dc4b70246da7f20d37248` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/shopify/shopify/shopify.list) |
| shadowrocket | `shadowrocket/shopify/shopify/shopify.list` | 16 | 448 | `a6649d50d571b65a5be41d294f1bc0036f60f39b3cdd79f010376faeff2433bc` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/shopify/shopify/shopify.list) |
| singbox | `singbox/shopify/shopify/shopify.json` | 0 | 481 | `89d2bfdb7e381bc2bd781d1a6de69127c636eb405d26a0306e0a5caecbddabff` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/shopify/shopify/shopify.json) |
| surge | `surge/shopify/shopify/shopify.list` | 16 | 448 | `a6649d50d571b65a5be41d294f1bc0036f60f39b3cdd79f010376faeff2433bc` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/shopify/shopify/shopify.list) |

## 4. 使用方法

选择客户端 → 复制对应 Raw → 加入客户端远程 Rule Set / Rule Provider / rule-set → 再绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用另一种格式的规则文件，也不要把 `rule/` 浏览树直接作为客户端运行时输入。

## 5. 服务集与独立子服务

服务集用于较宽覆盖；独立子服务用于精确分流。父级与子级同时存在时，实际命中关系由客户端规则顺序决定。

## 6. 图标来源与安全规则

真实品牌图标优先；缺失品牌身份时只使用 semantic fallback。禁止把风格化 fallback 冒充品牌官方 Logo，禁止用 favicon 作为永久主图标。

## 7. 完整性检查

| 项目 | SSOT |
|---|---|
| 服务 ID / 语义规则数 / SHA-256 | `rule/_index.yaml` |
| 客户端文件 / rule_count / size / SHA-256 | `generated/manifest.json` |
| 图标主层 / fallback | `assets/icons/v4/service-index.json` |
| 当前图标 Release | `assets/icons/v4/release-pointer.json` |

本页属于派生文档，不要手工维护发行数字、Raw、SHA 或图标地址。

## 8. 相关入口

- [服务总目录](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/SERVICE_CATALOG.md)
- [V4 图标库说明](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/assets/icons/v4/README.md)
- [完整使用说明](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/RULE_USAGE_GUIDE.md)
- [Icon Usage](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/ICON_USAGE.md)

[回到顶部](#top)