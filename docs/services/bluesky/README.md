<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/bluesky.png" alt="Bluesky 图标" width="72" height="72">

# Bluesky — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `bluesky_aggregate` |
| 类型 | provider_aggregate |
| Provider | `bluesky` |
| 语义规则数量 | **3** |
| 语义 SHA-256 | `fd8da727021a35f8d5769743ae5103f8884bbc209d7edc6ec81f3675ddcc99a7` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.bluesky`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/bluesky.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/bluesky/bluesky.yaml` | 3 | 71 | `af35b15e50bb7698f17a069986a134f5b3a3f812976cf27a22d7de2a34571794` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/bluesky/bluesky.yaml) |
| loon | `loon/bluesky/bluesky.list` | 3 | 76 | `0a0b32013696b2a6403a1b017094599e5516bf2d7d861ffa03ca77cbdcbff5b7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/bluesky/bluesky.list) |
| mihomo | `mihomo/bluesky/bluesky.yaml` | 3 | 97 | `869deeff312edc3e52c848d58afde54ceae7bbe97ee2c3f20c56be6ad714871e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/bluesky/bluesky.yaml) |
| quantumultx | `quantumultx/bluesky/bluesky.list` | 3 | 94 | `f6d3554e6d9e870927997a5f2c8460047d598be2f60aa9a5a2df7b8b1b401d4f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/bluesky/bluesky.list) |
| shadowrocket | `shadowrocket/bluesky/bluesky.list` | 3 | 76 | `0a0b32013696b2a6403a1b017094599e5516bf2d7d861ffa03ca77cbdcbff5b7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/bluesky/bluesky.list) |
| singbox | `singbox/bluesky/bluesky.json` | 0 | 148 | `300c28fa12cbd7017e60e209d133decd438d1c36145f5408ba5caf8e47911d8c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/bluesky/bluesky.json) |
| surge | `surge/bluesky/bluesky.list` | 3 | 76 | `0a0b32013696b2a6403a1b017094599e5516bf2d7d861ffa03ca77cbdcbff5b7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/bluesky/bluesky.list) |

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