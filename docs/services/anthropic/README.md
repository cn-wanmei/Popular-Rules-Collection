<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/anthropic.png" alt="Anthropic 图标" width="72" height="72">

# Anthropic — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `anthropic_aggregate` |
| 类型 | provider_aggregate |
| Provider | `anthropic` |
| 语义规则数量 | **9** |
| 语义 SHA-256 | `3b3fa161786fef0e7949ff6fe5fbd59c7cd1f4f389f19ada781ec31e321f71bb` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.anthropic`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/anthropic.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/anthropic/anthropic.yaml` | 9 | 259 | `6d08dc3118aa45c9c6b9a68891960d84aa9f74a3cff8b81ce7ea064173aea778` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/anthropic/anthropic.yaml) |
| loon | `loon/anthropic/anthropic.list` | 9 | 293 | `3138a28adfae2ae9280dbc69687b8d90ecb00081c3e1c2c2c4f488f10613f5bd` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/anthropic/anthropic.list) |
| mihomo | `mihomo/anthropic/anthropic.yaml` | 9 | 338 | `d941ca7b4fe94b003df1197ed64ad27586aa8bbea35cf8421c59e2ee32a92182` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/anthropic/anthropic.yaml) |
| quantumultx | `quantumultx/anthropic/anthropic.list` | 9 | 347 | `07e236d886e60a4e5efd6b2cff4d685a4735d937b0f85731efb7586c34fa6f71` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/anthropic/anthropic.list) |
| shadowrocket | `shadowrocket/anthropic/anthropic.list` | 9 | 293 | `3138a28adfae2ae9280dbc69687b8d90ecb00081c3e1c2c2c4f488f10613f5bd` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/anthropic/anthropic.list) |
| singbox | `singbox/anthropic/anthropic.json` | 0 | 380 | `34fdcb9c288664bc3f3e5bd93453db8990bcb81681fb27c6f6038a275285e70f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/anthropic/anthropic.json) |
| surge | `surge/anthropic/anthropic.list` | 9 | 293 | `3138a28adfae2ae9280dbc69687b8d90ecb00081c3e1c2c2c4f488f10613f5bd` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/anthropic/anthropic.list) |

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