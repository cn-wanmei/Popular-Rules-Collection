<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/netlify.png" alt="Netlify 图标" width="72" height="72">

# Netlify — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `netlify` |
| 类型 | service |
| Provider | `netlify` |
| 语义规则数量 | **10** |
| 语义 SHA-256 | `50574211f809a3723f4ee598c6e99f63b8d4db545deb36ec9f45553798988373` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.netlify`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/netlify.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/netlify/netlify/netlify.yaml` | 10 | 298 | `2405e762ffa2901296f76664a16013757579ddc47433f919e13f37161f8d93d0` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/netlify/netlify/netlify.yaml) |
| loon | `loon/netlify/netlify/netlify.list` | 10 | 359 | `e60a01dd5e231ca1b500053e53670965a8390577988ff6bc8fdc54ae315425cd` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/netlify/netlify/netlify.list) |
| mihomo | `mihomo/netlify/netlify/netlify.yaml` | 10 | 408 | `ce00b6131e10b78802d24682f9b41af863d9e18617c07c1b8c10272961b924b1` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/netlify/netlify/netlify.yaml) |
| quantumultx | `quantumultx/netlify/netlify/netlify.list` | 10 | 419 | `3f320e35eb4f3261e0fe8f17ded303c6e2af3a9e6bdaa4a0107dc377b94fc501` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/netlify/netlify/netlify.list) |
| shadowrocket | `shadowrocket/netlify/netlify/netlify.list` | 10 | 359 | `e60a01dd5e231ca1b500053e53670965a8390577988ff6bc8fdc54ae315425cd` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/netlify/netlify/netlify.list) |
| singbox | `singbox/netlify/netlify/netlify.json` | 0 | 410 | `12b1f086f3c7bcbabe7025bfa3fe918047b21677a1345064923d24a9eb383db7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/netlify/netlify/netlify.json) |
| surge | `surge/netlify/netlify/netlify.list` | 10 | 359 | `e60a01dd5e231ca1b500053e53670965a8390577988ff6bc8fdc54ae315425cd` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/netlify/netlify/netlify.list) |

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