<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/playstation.png" alt="PlayStation 图标" width="72" height="72">

# PlayStation — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `playstation` |
| 类型 | service |
| Provider | `playstation` |
| 语义规则数量 | **4** |
| 语义 SHA-256 | `160449d533de2fd786a2c3d2d575b4df1b0c3bab1444afb2125afcbe031ba0e7` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.playstation`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/playstation.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/playstation/playstation/playstation.yaml` | 4 | 127 | `de94e368df138979b309f7f1cd0591c2aa5b00ebb4df6f397a25a7d3906069cc` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/playstation/playstation/playstation.yaml) |
| loon | `loon/playstation/playstation/playstation.list` | 4 | 140 | `7ea8a5184a0c0eb7f2ffbeb6a7e6117f6cb4e34b9f4da03cb7a610ae694a66f6` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/playstation/playstation/playstation.list) |
| mihomo | `mihomo/playstation/playstation/playstation.yaml` | 4 | 165 | `2f1a0803b7223f6ac6154f3515efd74aceab9b4822778df6b65cf390a03428ed` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/playstation/playstation/playstation.yaml) |
| quantumultx | `quantumultx/playstation/playstation/playstation.list` | 4 | 164 | `ff89f81774705a628cfd91e253a2dcf970d82c32d397ed2acf10e003cbb250da` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/playstation/playstation/playstation.list) |
| shadowrocket | `shadowrocket/playstation/playstation/playstation.list` | 4 | 140 | `7ea8a5184a0c0eb7f2ffbeb6a7e6117f6cb4e34b9f4da03cb7a610ae694a66f6` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/playstation/playstation/playstation.list) |
| singbox | `singbox/playstation/playstation/playstation.json` | 0 | 209 | `11efcdcb3efc47cba292d82c7de523f84833b228745e1f5a4788f3c3f432c515` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/playstation/playstation/playstation.json) |
| surge | `surge/playstation/playstation/playstation.list` | 4 | 140 | `7ea8a5184a0c0eb7f2ffbeb6a7e6117f6cb4e34b9f4da03cb7a610ae694a66f6` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/playstation/playstation/playstation.list) |

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