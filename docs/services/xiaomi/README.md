<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/xiaomi.png" alt="Xiaomi 图标" width="72" height="72">

# Xiaomi — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `xiaomi` |
| 类型 | provider_aggregate |
| Provider | `xiaomi` |
| 语义规则数量 | **159** |
| 语义 SHA-256 | `089753b4ce48e8fd1a3ec568359696263d3a5e6c9b2a65fa03354de770feec5e` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.xiaomi`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/xiaomi.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/xiaomi/xiaomi.yaml` | 157 | 3239 | `9c1fd9283e5706b5efaee32f18d135cf473066ef4b8ad7785bd7dad667805d6c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/xiaomi/xiaomi.yaml) |
| loon | `loon/xiaomi/xiaomi.list` | 157 | 4409 | `c2f8dd097a98adcc2bdba503fdd3dd7e25ec96121f78d100bb240a814e9245d9` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/xiaomi/xiaomi.list) |
| mihomo | `mihomo/xiaomi/xiaomi.yaml` | 157 | 5046 | `cc4545047d1a6073f1ff2e95d2cb9315c8f23178a0d22901af9dc3e28297babd` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/xiaomi/xiaomi.yaml) |
| quantumultx | `quantumultx/xiaomi/xiaomi.list` | 157 | 5369 | `efab0498a0f6fb7c4198e85fd25f5e866530ea2bfe1667abe1d5c0a7e2aabb85` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/xiaomi/xiaomi.list) |
| shadowrocket | `shadowrocket/xiaomi/xiaomi.list` | 157 | 4409 | `c2f8dd097a98adcc2bdba503fdd3dd7e25ec96121f78d100bb240a814e9245d9` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/xiaomi/xiaomi.list) |
| singbox | `singbox/xiaomi/xiaomi.json` | 0 | 4100 | `b69b64933ae8bbd5fa819e1a43db3bd669fa7bf42096cf811250900ca09e02ca` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/xiaomi/xiaomi.json) |
| surge | `surge/xiaomi/xiaomi.list` | 157 | 4409 | `c2f8dd097a98adcc2bdba503fdd3dd7e25ec96121f78d100bb240a814e9245d9` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/xiaomi/xiaomi.list) |

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