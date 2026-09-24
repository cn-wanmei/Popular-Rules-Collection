<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/zhihu.png" alt="Zhihu 图标" width="72" height="72">

# Zhihu — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `zhihu` |
| 类型 | service |
| Provider | `zhihu` |
| 语义规则数量 | **7** |
| 语义 SHA-256 | `31e9453b865fda2d9b4f24c35762146485d8c38da1eb30a0b32381ff72d4686b` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.zhihu`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/zhihu.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/zhihu/zhihu/zhihu.yaml` | 7 | 221 | `eca9e15ad50c678e0c9209da6025b10684054e996156d8c0b94799e64a0329e9` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/zhihu/zhihu/zhihu.yaml) |
| loon | `loon/zhihu/zhihu/zhihu.list` | 7 | 202 | `052d51c68cfee444ed9701d2d165262325ac5e472b8fb0a5de5664fa0d9b4253` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/zhihu/zhihu/zhihu.list) |
| mihomo | `mihomo/zhihu/zhihu/zhihu.yaml` | 7 | 239 | `2d271eec1f5f70f44fe44b832d5afeb59666a51ab624a54c937ba16906a8cdd2` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/zhihu/zhihu/zhihu.yaml) |
| quantumultx | `quantumultx/zhihu/zhihu/zhihu.list` | 7 | 254 | `5107dc79e992c960394908947fefbd21eeb3a46ac42b2323463ca169ac90bb0a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/zhihu/zhihu/zhihu.list) |
| shadowrocket | `shadowrocket/zhihu/zhihu/zhihu.list` | 7 | 202 | `052d51c68cfee444ed9701d2d165262325ac5e472b8fb0a5de5664fa0d9b4253` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/zhihu/zhihu/zhihu.list) |
| singbox | `singbox/zhihu/zhihu/zhihu.json` | 0 | 318 | `3e693850927d251165be4f8c79409dce11c1e66a5ca9d6b6547a6cfed19ddbaa` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/zhihu/zhihu/zhihu.json) |
| surge | `surge/zhihu/zhihu/zhihu.list` | 7 | 202 | `052d51c68cfee444ed9701d2d165262325ac5e472b8fb0a5de5664fa0d9b4253` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/zhihu/zhihu/zhihu.list) |

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