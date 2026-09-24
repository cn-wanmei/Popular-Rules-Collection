<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/twitter.png" alt="Twitter 图标" width="72" height="72">

# Twitter — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `twitter` |
| 类型 | service |
| Provider | `twitter` |
| 语义规则数量 | **34** |
| 语义 SHA-256 | `3137e87c0363f28022a4c32a6dcb664336016bd5ed6bfe2d070b81fab34ccd7d` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.twitter`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/twitter.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/twitter/twitter/twitter.yaml` | 81 | 1614 | `31f799c7142e460da5cddd705d8ff22e3c3b5b3016d29db953a0fbd3b24f2ef0` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/twitter/twitter/twitter.yaml) |
| loon | `loon/twitter/twitter/twitter.list` | 81 | 2175 | `e9ce43da284b18c7d69dec0d0f054feef7e123a3b35bea52323f15344b064183` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/twitter/twitter/twitter.list) |
| mihomo | `mihomo/twitter/twitter/twitter.yaml` | 81 | 2508 | `0c42f7a70ea7cf6efe1df461b0527e32757445a2c3f3036a8b1480190438bc2a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/twitter/twitter/twitter.yaml) |
| quantumultx | `quantumultx/twitter/twitter/twitter.list` | 81 | 2673 | `2ff8a73ef293aff60c171845c85848fe427d62371af8e16bbe77da30b5686651` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/twitter/twitter/twitter.list) |
| shadowrocket | `shadowrocket/twitter/twitter/twitter.list` | 81 | 2175 | `e9ce43da284b18c7d69dec0d0f054feef7e123a3b35bea52323f15344b064183` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/twitter/twitter/twitter.list) |
| singbox | `singbox/twitter/twitter/twitter.json` | 0 | 2109 | `334bf291055502569fdeb2624a9a4e05275e8f0d51b690424e7e8f609820bab1` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/twitter/twitter/twitter.json) |
| surge | `surge/twitter/twitter/twitter.list` | 81 | 2175 | `e9ce43da284b18c7d69dec0d0f054feef7e123a3b35bea52323f15344b064183` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/twitter/twitter/twitter.list) |

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