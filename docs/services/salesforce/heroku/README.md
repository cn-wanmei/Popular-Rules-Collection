<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/heroku.png" alt="Heroku 图标" width="72" height="72">

# Heroku — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `heroku` |
| 类型 | service |
| Provider | `salesforce` |
| 语义规则数量 | **12** |
| 语义 SHA-256 | `ea762d1a2e9bcd2ecc67b0f5cb32a5fe72917ecdced93e80e9cea37b6fb17f78` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.heroku`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/heroku.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/salesforce/heroku/heroku.yaml` | 24 | 471 | `fa73560f93d577daefc466ae75eda685bc83b1d400710f851661feb2cebd1751` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/salesforce/heroku/heroku.yaml) |
| loon | `loon/salesforce/heroku/heroku.list` | 24 | 644 | `ea83ba35848c92cc243640b5b08595dc9af25cf8f3bbc1829bc66c288678f9dc` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/salesforce/heroku/heroku.list) |
| mihomo | `mihomo/salesforce/heroku/heroku.yaml` | 24 | 749 | `61ffdbe3ef0c382a48edeef472c19e6272cbc24db3c315ab3746a8d104ad7ee5` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/salesforce/heroku/heroku.yaml) |
| quantumultx | `quantumultx/salesforce/heroku/heroku.list` | 24 | 788 | `7bf090c72af2b122d7466ff67b314ed970937e25a086c896005fc49537e8d27f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/salesforce/heroku/heroku.list) |
| shadowrocket | `shadowrocket/salesforce/heroku/heroku.list` | 24 | 644 | `ea83ba35848c92cc243640b5b08595dc9af25cf8f3bbc1829bc66c288678f9dc` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/salesforce/heroku/heroku.list) |
| singbox | `singbox/salesforce/heroku/heroku.json` | 0 | 653 | `46c2decccb96cdc89b51c6c801859196b741c5cb18116c4e9e34e1ffe43e2d40` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/salesforce/heroku/heroku.json) |
| surge | `surge/salesforce/heroku/heroku.list` | 24 | 644 | `ea83ba35848c92cc243640b5b08595dc9af25cf8f3bbc1829bc66c288678f9dc` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/salesforce/heroku/heroku.list) |

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