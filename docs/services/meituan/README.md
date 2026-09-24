<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/meituan.png" alt="Meituan 图标" width="72" height="72">

# Meituan — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `meituan_aggregate` |
| 类型 | provider_aggregate |
| Provider | `meituan` |
| 语义规则数量 | **7** |
| 语义 SHA-256 | `3dc50e6fde9522aae561e00233edb2cf63463ba3aa6d9be6e16d48a963245f8d` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.meituan`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/meituan.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/meituan/meituan.yaml` | 7 | 141 | `9e5194ad7ac639b7f50f3302c326adc7ca3eba02751e0be3948a2d71490d4d9e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/meituan/meituan.yaml) |
| loon | `loon/meituan/meituan.list` | 7 | 178 | `c82710dcc7c796e3adcedc38a9ff867e6c8b0a210fca3f277a2821cbd720f2d0` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/meituan/meituan.list) |
| mihomo | `mihomo/meituan/meituan.yaml` | 7 | 215 | `22c6fa4e4d5ebd26e52962b1b73f730b5b0ac62ba276fd2720650e05e1cc9765` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/meituan/meituan.yaml) |
| quantumultx | `quantumultx/meituan/meituan.list` | 7 | 220 | `e0755b5c2d994237b7277a32107ff3dc00e7fd540e229e393b81ab7c728c38c6` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/meituan/meituan.list) |
| shadowrocket | `shadowrocket/meituan/meituan.list` | 7 | 178 | `c82710dcc7c796e3adcedc38a9ff867e6c8b0a210fca3f277a2821cbd720f2d0` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/meituan/meituan.list) |
| singbox | `singbox/meituan/meituan.json` | 0 | 238 | `94ddeff558bdfc36a12334e23bc54bc435731a420173cefb8058be52ad88e718` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/meituan/meituan.json) |
| surge | `surge/meituan/meituan.list` | 7 | 178 | `c82710dcc7c796e3adcedc38a9ff867e6c8b0a210fca3f277a2821cbd720f2d0` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/meituan/meituan.list) |

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