<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/remix/service.svg" alt="HoYoverse 图标" width="72" height="72">

# HoYoverse — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `hoyoverse` |
| 类型 | provider_aggregate |
| Provider | `hoyoverse` |
| 语义规则数量 | **15** |
| 语义 SHA-256 | `c388eb7a46fdb761fdf0ec6c550a83b9daf81f5be3e4dd1d170694525e8cedf5` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**remix semantic fallback**

- Style：`remix`
- Identity：`semantic.fallback.remix`
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/remix/service.svg`
- 该图标用于覆盖缺失身份，不代表官方品牌 Logo。

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/hoyoverse/hoyoverse.yaml` | 15 | 316 | `3c57ea17c346f48c681a7be5485d80458931815b2218bf9f145dc472088ffefe` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/hoyoverse/hoyoverse.yaml) |
| loon | `loon/hoyoverse/hoyoverse.list` | 15 | 417 | `081508eedd23c8837ba0f4affade3af19b34fe8c07234a70f8b62a1e513af00a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/hoyoverse/hoyoverse.list) |
| mihomo | `mihomo/hoyoverse/hoyoverse.yaml` | 15 | 486 | `79d1801332469c3521be5aec3678bc2fc5dc8ee84ba14000fc26bb9ac83a9e1f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/hoyoverse/hoyoverse.yaml) |
| quantumultx | `quantumultx/hoyoverse/hoyoverse.list` | 15 | 507 | `f412dd6b37c5e7b071ed6e9d0bb829ae0b9e913216ebf571214c4aa69dd881e6` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/hoyoverse/hoyoverse.list) |
| shadowrocket | `shadowrocket/hoyoverse/hoyoverse.list` | 15 | 417 | `081508eedd23c8837ba0f4affade3af19b34fe8c07234a70f8b62a1e513af00a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/hoyoverse/hoyoverse.list) |
| singbox | `singbox/hoyoverse/hoyoverse.json` | 0 | 453 | `07f786aa886835d9ba9df035ca21b97eee6b9a40c3dd36f5e4072752bc20fbb9` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/hoyoverse/hoyoverse.json) |
| surge | `surge/hoyoverse/hoyoverse.list` | 15 | 417 | `081508eedd23c8837ba0f4affade3af19b34fe8c07234a70f8b62a1e513af00a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/hoyoverse/hoyoverse.list) |

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