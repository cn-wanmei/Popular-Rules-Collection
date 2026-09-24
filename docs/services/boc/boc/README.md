<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/heroicons/service.svg" alt="Bank of China 图标" width="72" height="72">

# Bank of China — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `boc` |
| 类型 | service |
| Provider | `boc` |
| 语义规则数量 | **22** |
| 语义 SHA-256 | `9d8f718b56311d370083db69c7fe4a755d969f9e14af060346ef3bc3b39042fa` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**heroicons semantic fallback**

- Style：`heroicons`
- Identity：`semantic.fallback.heroicons`
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/heroicons/service.svg`
- 该图标用于覆盖缺失身份，不代表官方品牌 Logo。

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/boc/boc/boc.yaml` | 22 | 455 | `c4007caf2b81d23f5518d212e9b0b566a6dfbcbd80a9bdffb93d74b2a230e6ed` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/boc/boc/boc.yaml) |
| loon | `loon/boc/boc/boc.list` | 22 | 612 | `751f78db55a0b5112b248b9d3d1fd153cfb11fceae1c4fa122ac8126f83db459` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/boc/boc/boc.list) |
| mihomo | `mihomo/boc/boc/boc.yaml` | 22 | 709 | `4ecb7ca1b2e01c30cbeaf977f1d2b86dd2797f58142afff02f02746fa537ca30` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/boc/boc/boc.yaml) |
| quantumultx | `quantumultx/boc/boc/boc.list` | 22 | 744 | `c5202eee9788fd9bf99e9af03591ea01f6e6b1bbc5c44b958ed4e0241c708f4a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/boc/boc/boc.list) |
| shadowrocket | `shadowrocket/boc/boc/boc.list` | 22 | 612 | `751f78db55a0b5112b248b9d3d1fd153cfb11fceae1c4fa122ac8126f83db459` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/boc/boc/boc.list) |
| singbox | `singbox/boc/boc/boc.json` | 0 | 627 | `4cdd53e56e76b3486b75c574406685415b9e9ebb67d7a1c31f41496b6581977f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/boc/boc/boc.json) |
| surge | `surge/boc/boc/boc.list` | 22 | 612 | `751f78db55a0b5112b248b9d3d1fd153cfb11fceae1c4fa122ac8126f83db459` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/boc/boc/boc.list) |

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