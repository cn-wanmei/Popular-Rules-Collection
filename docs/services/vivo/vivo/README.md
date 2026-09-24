<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/vivo.png" alt="vivo 图标" width="72" height="72">

# vivo — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `vivo` |
| 类型 | service |
| Provider | `vivo` |
| 语义规则数量 | **14** |
| 语义 SHA-256 | `12b5d8915023ba7ca34ca2f18f41b35a5e698cca4f9e22d2e2301f311e2b21ba` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.vivo`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/vivo.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/vivo/vivo/vivo.yaml` | 14 | 258 | `0cf2d8e071427b31c9a6e071255ca1b8a0424ad5e5a6bfa386a474e68e2e81e3` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/vivo/vivo/vivo.yaml) |
| loon | `loon/vivo/vivo/vivo.list` | 14 | 351 | `a938c5e0820f3358dfc7ce16e4988687244ac64adf2ef954cac7eceb2fac7892` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/vivo/vivo/vivo.list) |
| mihomo | `mihomo/vivo/vivo/vivo.yaml` | 14 | 416 | `c635ce22f118fcb3eb896116d5c1ddc3e7418b1e5f5df0f12b5e2ab906131b40` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/vivo/vivo/vivo.yaml) |
| quantumultx | `quantumultx/vivo/vivo/vivo.list` | 14 | 435 | `9cef4a73bf7914c22bcaac78f87a65a119bd1692c1780a4e54321dcc5171f2f7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/vivo/vivo/vivo.list) |
| shadowrocket | `shadowrocket/vivo/vivo/vivo.list` | 14 | 351 | `a938c5e0820f3358dfc7ce16e4988687244ac64adf2ef954cac7eceb2fac7892` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/vivo/vivo/vivo.list) |
| singbox | `singbox/vivo/vivo/vivo.json` | 0 | 390 | `fb43f7cf3013ffa29f11720d4889f78bcddcf6bb7f8b3491011b185c31ef3c04` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/vivo/vivo/vivo.json) |
| surge | `surge/vivo/vivo/vivo.list` | 14 | 351 | `a938c5e0820f3358dfc7ce16e4988687244ac64adf2ef954cac7eceb2fac7892` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/vivo/vivo/vivo.list) |

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