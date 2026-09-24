<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/soundcloud.png" alt="SoundCloud 图标" width="72" height="72">

# SoundCloud — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `soundcloud` |
| 类型 | service |
| Provider | `soundcloud` |
| 语义规则数量 | **5** |
| 语义 SHA-256 | `3d3ac172e3cea92ca5d1456dabc95e2ff9bdee16fe1c5de5c50ef6b6b82e0de4` |
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
| egern | `egern/soundcloud/soundcloud/soundcloud.yaml` | 7 | 163 | `64df87d1c873fd65a62551d5e07cba9ae9e9fa4d53b78febaad7d40557a9d592` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/soundcloud/soundcloud/soundcloud.yaml) |
| loon | `loon/soundcloud/soundcloud/soundcloud.list` | 7 | 200 | `1b589486f405c9aef2f9127ab095fbcf04347c92a41121d8776fed1fd0073daa` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/soundcloud/soundcloud/soundcloud.list) |
| mihomo | `mihomo/soundcloud/soundcloud/soundcloud.yaml` | 7 | 237 | `c5ee56969ea12573ef7593227849beae20b212c959b974d6e92add82c5375c3d` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/soundcloud/soundcloud/soundcloud.yaml) |
| quantumultx | `quantumultx/soundcloud/soundcloud/soundcloud.list` | 7 | 242 | `8d686f73e3459e80ec578a000228603f6a215062e7e902f5522d47b30f0649ca` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/soundcloud/soundcloud/soundcloud.list) |
| shadowrocket | `shadowrocket/soundcloud/soundcloud/soundcloud.list` | 7 | 200 | `1b589486f405c9aef2f9127ab095fbcf04347c92a41121d8776fed1fd0073daa` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/soundcloud/soundcloud/soundcloud.list) |
| singbox | `singbox/soundcloud/soundcloud/soundcloud.json` | 0 | 260 | `ed59b60dc5801751b6cc1494839e92fce024493173d1e6f0a9729352ba897a48` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/soundcloud/soundcloud/soundcloud.json) |
| surge | `surge/soundcloud/soundcloud/soundcloud.list` | 7 | 200 | `1b589486f405c9aef2f9127ab095fbcf04347c92a41121d8776fed1fd0073daa` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/soundcloud/soundcloud/soundcloud.list) |

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