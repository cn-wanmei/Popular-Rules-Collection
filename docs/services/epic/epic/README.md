<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/epic.png" alt="Epic Games 图标" width="72" height="72">

# Epic Games — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `epic` |
| 类型 | service |
| Provider | `epic` |
| 语义规则数量 | **15** |
| 语义 SHA-256 | `530a2dec55dd3d8ee3b6f8576cfcaada7cae8a1ece7e4059a6b002a8ecdd625e` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.epic`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/epic.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/epic/epic/epic.yaml` | 15 | 332 | `14a9b02403c0d7b6a0cd209c90c91727d8058654b155fbc4f7b9f988c9c67517` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/epic/epic/epic.yaml) |
| loon | `loon/epic/epic/epic.list` | 15 | 433 | `7996135bc776b0d0ba2cdd4a2474bc3604e5a6dc3a95f03a2fe88bfe79b573ea` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/epic/epic/epic.list) |
| mihomo | `mihomo/epic/epic/epic.yaml` | 15 | 502 | `6d43f71aa08c2013cf7b3396b1e480c9028b88670567650bf08d81659dd5c923` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/epic/epic/epic.yaml) |
| quantumultx | `quantumultx/epic/epic/epic.list` | 15 | 523 | `7c4e1bd4758304f48c7c306957081bf3c86455c67a1993c34b1bec07a252ba7f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/epic/epic/epic.list) |
| shadowrocket | `shadowrocket/epic/epic/epic.list` | 15 | 433 | `7996135bc776b0d0ba2cdd4a2474bc3604e5a6dc3a95f03a2fe88bfe79b573ea` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/epic/epic/epic.list) |
| singbox | `singbox/epic/epic/epic.json` | 0 | 469 | `79c34363f71f3930cd89aa4fb99d474cdf055e14210607f0ebaa39242ef513f5` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/epic/epic/epic.json) |
| surge | `surge/epic/epic/epic.list` | 15 | 433 | `7996135bc776b0d0ba2cdd4a2474bc3604e5a6dc3a95f03a2fe88bfe79b573ea` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/epic/epic/epic.list) |

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