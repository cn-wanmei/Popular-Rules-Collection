<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/jetbrains.png" alt="JetBrains 图标" width="72" height="72">

# JetBrains — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `jetbrains_aggregate` |
| 类型 | provider_aggregate |
| Provider | `jetbrains` |
| 语义规则数量 | **25** |
| 语义 SHA-256 | `fe6be2518ee347f1ae32eef31dccbd99d645c55a141414e2e4c814a042c6662b` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.jetbrains`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/jetbrains.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/jetbrains/jetbrains.yaml` | 25 | 508 | `86d0293e2edc38abc818333ec50038c440abf6916b07a8944778092c9f607e7e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/jetbrains/jetbrains.yaml) |
| loon | `loon/jetbrains/jetbrains.list` | 25 | 689 | `48f53f799b186f18d8cc28d60830c07ab369db05776ec00706b6d732076dd8bb` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/jetbrains/jetbrains.list) |
| mihomo | `mihomo/jetbrains/jetbrains.yaml` | 25 | 798 | `18a7646f1a52a9075da31bb98b3dbf4111cf5afb7cce44a54d23a6f6df4285c4` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/jetbrains/jetbrains.yaml) |
| quantumultx | `quantumultx/jetbrains/jetbrains.list` | 25 | 839 | `bba3f0bab49cad1ea8f1257e05a01079c571d6b13d55ff6fdee7bcf8696e7871` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/jetbrains/jetbrains.list) |
| shadowrocket | `shadowrocket/jetbrains/jetbrains.list` | 25 | 689 | `48f53f799b186f18d8cc28d60830c07ab369db05776ec00706b6d732076dd8bb` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/jetbrains/jetbrains.list) |
| singbox | `singbox/jetbrains/jetbrains.json` | 0 | 695 | `a8ced873ec06bda6d99bf296ed82cd713e29a813e0b58616d9e7cf864bf679d4` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/jetbrains/jetbrains.json) |
| surge | `surge/jetbrains/jetbrains.list` | 25 | 689 | `48f53f799b186f18d8cc28d60830c07ab369db05776ec00706b6d732076dd8bb` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/jetbrains/jetbrains.list) |

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