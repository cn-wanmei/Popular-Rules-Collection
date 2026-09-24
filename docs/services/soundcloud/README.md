<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/soundcloud.png" alt="SoundCloud 图标" width="72" height="72">

# SoundCloud — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `soundcloud_aggregate` |
| 类型 | provider_aggregate |
| Provider | `soundcloud` |
| 语义规则数量 | **5** |
| 语义 SHA-256 | `d55ed6b4630b251af084915af87162df2a375571a13b1e708bb4592847d8eb74` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.soundcloud`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/soundcloud.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/soundcloud/soundcloud.yaml` | 5 | 125 | `d8505d26d71330ad272415ec17789ab53791f59fc456e2422dd80b7c2e479d5b` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/soundcloud/soundcloud.yaml) |
| loon | `loon/soundcloud/soundcloud.list` | 5 | 146 | `b42a455a035f0f68541370393247e619724a5a597acb18d71813be3e2a945c24` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/soundcloud/soundcloud.list) |
| mihomo | `mihomo/soundcloud/soundcloud.yaml` | 5 | 175 | `ad5991a95fc7a7381b0d3069f65104f57c2eec336d261ac406535a6715918125` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/soundcloud/soundcloud.yaml) |
| quantumultx | `quantumultx/soundcloud/soundcloud.list` | 5 | 176 | `83554a4e1e97df7fa0a6abd801c38aa26c8a21a2503745b6c4b8aa43d3721a1e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/soundcloud/soundcloud.list) |
| shadowrocket | `shadowrocket/soundcloud/soundcloud.list` | 5 | 146 | `b42a455a035f0f68541370393247e619724a5a597acb18d71813be3e2a945c24` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/soundcloud/soundcloud.list) |
| singbox | `singbox/soundcloud/soundcloud.json` | 0 | 212 | `f2c161abea69993e8da943d9e73d7248c36ac176d7276ab0fee72bceabb557c1` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/soundcloud/soundcloud.json) |
| surge | `surge/soundcloud/soundcloud.list` | 5 | 146 | `b42a455a035f0f68541370393247e619724a5a597acb18d71813be3e2a945c24` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/soundcloud/soundcloud.list) |

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