<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/cursor.png" alt="Cursor 图标" width="72" height="72">

# Cursor — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `cursor_aggregate` |
| 类型 | provider_aggregate |
| Provider | `cursor` |
| 语义规则数量 | **4** |
| 语义 SHA-256 | `a2cd7b706552620e342574e4c10eaba7944e9d0d4abdd143d2ef905033e5c74b` |
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
| egern | `egern/cursor/cursor.yaml` | 4 | 93 | `997c71bcbfd2601cda9e3a99c0a23d27d5f977913234552086912b86b09fcc39` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/cursor/cursor.yaml) |
| loon | `loon/cursor/cursor.list` | 4 | 106 | `cf6d3b7d5e7676c85bdc5a2ac0c8df34e27e99ca6c0276e06791b0aa5969ca3e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/cursor/cursor.list) |
| mihomo | `mihomo/cursor/cursor.yaml` | 4 | 131 | `33eaacd59faf5db8d7f3903f21d1bcf0f45a7496a4fa2f4281257f3f190786a3` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/cursor/cursor.yaml) |
| quantumultx | `quantumultx/cursor/cursor.list` | 4 | 130 | `b9d3e89469ad52b06d7c1e45daf4027e187af65341e769665110752720e6d4a3` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/cursor/cursor.list) |
| shadowrocket | `shadowrocket/cursor/cursor.list` | 4 | 106 | `cf6d3b7d5e7676c85bdc5a2ac0c8df34e27e99ca6c0276e06791b0aa5969ca3e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/cursor/cursor.list) |
| singbox | `singbox/cursor/cursor.json` | 0 | 175 | `8a5bf410a8e6d3c8cf71918cddec42cee6fdf5a11906c17ccedf20a749c56170` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/cursor/cursor.json) |
| surge | `surge/cursor/cursor.list` | 4 | 106 | `cf6d3b7d5e7676c85bdc5a2ac0c8df34e27e99ca6c0276e06791b0aa5969ca3e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/cursor/cursor.list) |

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