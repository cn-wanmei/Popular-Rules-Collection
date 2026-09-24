<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/cursor.png" alt="Cursor 图标" width="72" height="72">

# Cursor — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `cursor` |
| 类型 | service |
| Provider | `cursor` |
| 语义规则数量 | **4** |
| 语义 SHA-256 | `d4e6c80225fd936f31547e24f705ddbb2582a499c8afa20c8bdf4d1259a43bc8` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.cursor`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/cursor.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/cursor/cursor/cursor.yaml` | 4 | 93 | `5799d734248317873ade6b8c13ff9d05f1da1bb79f86c1e1afc4a6bf97c6c384` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/cursor/cursor/cursor.yaml) |
| loon | `loon/cursor/cursor/cursor.list` | 4 | 106 | `5c6d8418ed48e513a8b5697bea5948ee954fca9f5f683d5ee9234b1258111ad2` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/cursor/cursor/cursor.list) |
| mihomo | `mihomo/cursor/cursor/cursor.yaml` | 4 | 131 | `3934afa5e3dcb892bd7c227fe5b018ea04d758faf764eb2babe78db386dca435` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/cursor/cursor/cursor.yaml) |
| quantumultx | `quantumultx/cursor/cursor/cursor.list` | 4 | 130 | `1a3fbe5d9787184def7436488aec2760cc7e732e0fede712f41f27c5167f705f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/cursor/cursor/cursor.list) |
| shadowrocket | `shadowrocket/cursor/cursor/cursor.list` | 4 | 106 | `5c6d8418ed48e513a8b5697bea5948ee954fca9f5f683d5ee9234b1258111ad2` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/cursor/cursor/cursor.list) |
| singbox | `singbox/cursor/cursor/cursor.json` | 0 | 175 | `06aedc61fa8a28f26e5a202969b6eb668d1d3652bd52eec2c138b35947b10848` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/cursor/cursor/cursor.json) |
| surge | `surge/cursor/cursor/cursor.list` | 4 | 106 | `5c6d8418ed48e513a8b5697bea5948ee954fca9f5f683d5ee9234b1258111ad2` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/cursor/cursor/cursor.list) |

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