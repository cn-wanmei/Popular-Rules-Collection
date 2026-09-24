<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/reddit.png" alt="Reddit 图标" width="72" height="72">

# Reddit — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `reddit_aggregate` |
| 类型 | provider_aggregate |
| Provider | `reddit` |
| 语义规则数量 | **15** |
| 语义 SHA-256 | `6dfe0bf5e6091593e7b2e3b40a9494a096f3dc8c028b2bf900d8015d4df2578b` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.reddit`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/reddit.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/reddit/reddit.yaml` | 15 | 383 | `2dc40e8ddf201ca11adbdf6a298888a7f4134e5b663cb1c7963fb5b927ffc1be` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/reddit/reddit.yaml) |
| loon | `loon/reddit/reddit.list` | 15 | 484 | `d55ecbd4de6ac5d8d9848484e4e3d8cf443fd1bf07afd695a845a0b1986aaa1f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/reddit/reddit.list) |
| mihomo | `mihomo/reddit/reddit.yaml` | 15 | 553 | `1342943f212b8a364cba78f1c05a8b1cd27af163a49b910f8fe8b72480b66c62` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/reddit/reddit.yaml) |
| quantumultx | `quantumultx/reddit/reddit.list` | 15 | 574 | `f93b1f50fa907e1ee576b124d3b80abb30574920ab27ba21c31cea1623489b21` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/reddit/reddit.list) |
| shadowrocket | `shadowrocket/reddit/reddit.list` | 15 | 484 | `d55ecbd4de6ac5d8d9848484e4e3d8cf443fd1bf07afd695a845a0b1986aaa1f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/reddit/reddit.list) |
| singbox | `singbox/reddit/reddit.json` | 0 | 520 | `a75a8729e8ac677fceaf05bde92fb7d0681a4d12ceae56863c2edd031859082a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/reddit/reddit.json) |
| surge | `surge/reddit/reddit.list` | 15 | 484 | `d55ecbd4de6ac5d8d9848484e4e3d8cf443fd1bf07afd695a845a0b1986aaa1f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/reddit/reddit.list) |

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