<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/appletv.png" alt="Apple TV 图标" width="72" height="72">

# Apple TV — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `appletv` |
| 类型 | service |
| Provider | `apple` |
| 语义规则数量 | **7** |
| 语义 SHA-256 | `357789e6ab42052ecaf5e433e1dc237bc003a90ae66fc9ce6b273dc72f8638e5` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.appletv`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/appletv.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/apple/appletv/appletv.yaml` | 7 | 215 | `a56cc6c3e54b51c251cfc2e75adec3ef34aef6a492ec22aa7a4edfc9dc2b4300` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/apple/appletv/appletv.yaml) |
| loon | `loon/apple/appletv/appletv.list` | 7 | 252 | `77616b096395fbee12c0d51e6cb284dfc6accc40a675e68c6cfdecb0f6622738` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/apple/appletv/appletv.list) |
| mihomo | `mihomo/apple/appletv/appletv.yaml` | 7 | 289 | `5b7d9702576f9c72f641a4516dc8a6a70f7f37f003b0e7ba18716411ca21a46f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/apple/appletv/appletv.yaml) |
| quantumultx | `quantumultx/apple/appletv/appletv.list` | 7 | 294 | `ddcb54f4b4a6aa8ef447cbbb7275839af0cde0c5b95aa25f339cde87154eae36` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/apple/appletv/appletv.list) |
| shadowrocket | `shadowrocket/apple/appletv/appletv.list` | 7 | 252 | `77616b096395fbee12c0d51e6cb284dfc6accc40a675e68c6cfdecb0f6622738` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/apple/appletv/appletv.list) |
| singbox | `singbox/apple/appletv/appletv.json` | 0 | 312 | `1a61a492dde21e2a0919564e64edd8bfd9bb62c886708c64fe0950d9e9eb4259` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/apple/appletv/appletv.json) |
| surge | `surge/apple/appletv/appletv.list` | 7 | 252 | `77616b096395fbee12c0d51e6cb284dfc6accc40a675e68c6cfdecb0f6622738` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/apple/appletv/appletv.list) |

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