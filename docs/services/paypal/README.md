<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/paypal.png" alt="PayPal 图标" width="72" height="72">

# PayPal — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `paypal_aggregate` |
| 类型 | provider_aggregate |
| Provider | `paypal` |
| 语义规则数量 | **247** |
| 语义 SHA-256 | `b9cc9c077c29f5f225c1943053a81f9c59b0c7eac1a51d1bc4eb69d0d3f07637` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.paypal`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/paypal.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/paypal/paypal.yaml` | 247 | 5707 | `0029376eafca1f7b978153379e4d2a6865bf865195803141f0c7f2410068ca8a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/paypal/paypal.yaml) |
| loon | `loon/paypal/paypal.list` | 247 | 7645 | `d6ca96cc7343b98be5b431dbbeb2e247e48c91ad26c9fbe8ae22bbd962469199` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/paypal/paypal.list) |
| mihomo | `mihomo/paypal/paypal.yaml` | 247 | 8642 | `b1e3346011b9953817bd8cb04511d2cd14faa8ef9119541b3e861d43a784503d` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/paypal/paypal.yaml) |
| quantumultx | `quantumultx/paypal/paypal.list` | 247 | 9127 | `80fefac88af5d641e11e52e122f6b7ab47f6cc7419c7255712b81db919f781a7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/paypal/paypal.list) |
| shadowrocket | `shadowrocket/paypal/paypal.list` | 247 | 7645 | `d6ca96cc7343b98be5b431dbbeb2e247e48c91ad26c9fbe8ae22bbd962469199` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/paypal/paypal.list) |
| singbox | `singbox/paypal/paypal.json` | 0 | 7018 | `373242602bdb6a1a7fd64dae6cbf1fd75ec53a21b0e415f9502f0378bdc81e7a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/paypal/paypal.json) |
| surge | `surge/paypal/paypal.list` | 247 | 7645 | `d6ca96cc7343b98be5b431dbbeb2e247e48c91ad26c9fbe8ae22bbd962469199` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/paypal/paypal.list) |

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