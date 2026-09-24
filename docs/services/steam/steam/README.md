<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/steam.png" alt="Steam 图标" width="72" height="72">

# Steam — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `steam` |
| 类型 | service |
| Provider | `steam` |
| 语义规则数量 | **84** |
| 语义 SHA-256 | `2895677e7a019d8568a9d95141eef7e05ea70eb3c31113f7137cf078581ed097` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.steam`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/steam.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/steam/steam/steam.yaml` | 120 | 3275 | `78e11762de2f14aef93ebbfc10854b33e7ae876c53b6dd19dc081d297bc6e7e8` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/steam/steam/steam.yaml) |
| loon | `loon/steam/steam/steam.list` | 120 | 4054 | `723bb13873470e5f2c3a7659287e5e897fcc14b3d3ae3ae78f4c0ade07ea10bf` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/steam/steam/steam.list) |
| mihomo | `mihomo/steam/steam/steam.yaml` | 120 | 4543 | `d1b27b6d9551686875aef4ddbf1dfe5b8df1afa3b129f37f21260bb3bdf09566` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/steam/steam/steam.yaml) |
| quantumultx | `quantumultx/steam/steam/steam.list` | 120 | 4774 | `a972a835caaeba8a4e1a8afa3e8cc4196ed61a0c38be42d62fe515b35c6d5f5e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/steam/steam/steam.list) |
| shadowrocket | `shadowrocket/steam/steam/steam.list` | 120 | 4054 | `723bb13873470e5f2c3a7659287e5e897fcc14b3d3ae3ae78f4c0ade07ea10bf` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/steam/steam/steam.list) |
| singbox | `singbox/steam/steam/steam.json` | 0 | 3965 | `90adf759fb5d3f2ad29d6f151f405d057fb3fefb78c192fb55eb3885670b9503` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/steam/steam/steam.json) |
| surge | `surge/steam/steam/steam.list` | 120 | 4054 | `723bb13873470e5f2c3a7659287e5e897fcc14b3d3ae3ae78f4c0ade07ea10bf` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/steam/steam/steam.list) |

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