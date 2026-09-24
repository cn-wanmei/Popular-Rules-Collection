<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/ebay.png" alt="eBay 图标" width="72" height="72">

# eBay — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `ebay` |
| 类型 | service |
| Provider | `ebay` |
| 语义规则数量 | **370** |
| 语义 SHA-256 | `0ef1731c090fae5f7b7d2d5d4d064cf40379b1b03cfb50812d25f0f5cfca561e` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.ebay`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/ebay.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/ebay/ebay/ebay.yaml` | 407 | 8293 | `5adf7844dd2899431840fe750d48cd2266b4b0d2cc133394b8948ab622539e9d` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/ebay/ebay/ebay.yaml) |
| loon | `loon/ebay/ebay/ebay.list` | 407 | 11511 | `1111383e1c2f82e6c6052882d27011021f84173e48aaaf67a05501b83022dd80` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/ebay/ebay/ebay.list) |
| mihomo | `mihomo/ebay/ebay/ebay.yaml` | 407 | 13148 | `5bbb02d25379f50ef1ed22667bfc2204901f116fbdac21139815b8f5add5df2a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/ebay/ebay/ebay.yaml) |
| quantumultx | `quantumultx/ebay/ebay/ebay.list` | 407 | 13953 | `f6cb21362ddb23f2f543e460d0f078ed171243ce81e65981055b6596f4d28c91` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/ebay/ebay/ebay.list) |
| shadowrocket | `shadowrocket/ebay/ebay/ebay.list` | 407 | 11511 | `1111383e1c2f82e6c6052882d27011021f84173e48aaaf67a05501b83022dd80` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/ebay/ebay/ebay.list) |
| singbox | `singbox/ebay/ebay/ebay.json` | 0 | 10404 | `9c9367b34ac7f01140f33d181c95c2850cf2fb023cefc28a62ebc2fef45a7d8f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/ebay/ebay/ebay.json) |
| surge | `surge/ebay/ebay/ebay.list` | 407 | 11511 | `1111383e1c2f82e6c6052882d27011021f84173e48aaaf67a05501b83022dd80` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/ebay/ebay/ebay.list) |

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