<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/walmart.png" alt="Walmart 图标" width="72" height="72">

# Walmart — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `walmart` |
| 类型 | service |
| Provider | `walmart` |
| 语义规则数量 | **10** |
| 语义 SHA-256 | `f1557d60e8b383f072d941faf2859b57b9b46fc24149126aaa9cb3d23ddad20c` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.walmart`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/walmart.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/walmart/walmart/walmart.yaml` | 10 | 220 | `40098999dc73dfb2cc6816f11cdcb4ed26c19aaf0cd1140b709d3ac9356e8c1a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/walmart/walmart/walmart.yaml) |
| loon | `loon/walmart/walmart/walmart.list` | 10 | 262 | `f4bea3ff567189517483082e3cd9359119f19c17b5ad795c31bb97b7205eb49c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/walmart/walmart/walmart.list) |
| mihomo | `mihomo/walmart/walmart/walmart.yaml` | 10 | 311 | `bc55d6f847ff9a5479c72d412f2e088ea1f45b959aaac201db67fb254c548b24` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/walmart/walmart/walmart.yaml) |
| quantumultx | `quantumultx/walmart/walmart/walmart.list` | 10 | 322 | `562830365590f7d1f279dcad7ba63334a8925e26fbef1f90fb6121980c38b333` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/walmart/walmart/walmart.list) |
| shadowrocket | `shadowrocket/walmart/walmart/walmart.list` | 10 | 262 | `f4bea3ff567189517483082e3cd9359119f19c17b5ad795c31bb97b7205eb49c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/walmart/walmart/walmart.list) |
| singbox | `singbox/walmart/walmart/walmart.json` | 0 | 346 | `142424615b828a266a01ece88280aaeb8382a42ae5475643c4178d9ceff2d67b` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/walmart/walmart/walmart.json) |
| surge | `surge/walmart/walmart/walmart.list` | 10 | 262 | `f4bea3ff567189517483082e3cd9359119f19c17b5ad795c31bb97b7205eb49c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/walmart/walmart/walmart.list) |

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