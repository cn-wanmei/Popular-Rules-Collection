<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/material-symbols/service.svg" alt="iQIYI 图标" width="72" height="72">

# iQIYI — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `iqiyi` |
| 类型 | service |
| Provider | `iqiyi` |
| 语义规则数量 | **67** |
| 语义 SHA-256 | `9c3fe6efe1d29dbebf89119d743735d24c1f7029b17693096164988923fb2094` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**material-symbols semantic fallback**

- Style：`material-symbols`
- Identity：`semantic.fallback.material-symbols`
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/material-symbols/service.svg`
- 该图标用于覆盖缺失身份，不代表官方品牌 Logo。

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/iqiyi/iqiyi/iqiyi.yaml` | 76 | 1522 | `b70beb2d5d0395646c12a43bb3ab8dccd0beaa410e99327bded231be40b26131` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/iqiyi/iqiyi/iqiyi.yaml) |
| loon | `loon/iqiyi/iqiyi/iqiyi.list` | 76 | 1953 | `247d0447bdad415f05924b96c617e077c567d7d4725b398f7462a13170594a09` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/iqiyi/iqiyi/iqiyi.list) |
| mihomo | `mihomo/iqiyi/iqiyi/iqiyi.yaml` | 76 | 2266 | `fd7f45f9ebf808e4458a258667d515e7c8d2fb4e5489f59a19335a5faf9012cd` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/iqiyi/iqiyi/iqiyi.yaml) |
| quantumultx | `quantumultx/iqiyi/iqiyi/iqiyi.list` | 76 | 2451 | `aff58480b95441c73c7a4d904693208858ba5edfcea8f3d25c34704329f1a145` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/iqiyi/iqiyi/iqiyi.list) |
| shadowrocket | `shadowrocket/iqiyi/iqiyi/iqiyi.list` | 76 | 1953 | `247d0447bdad415f05924b96c617e077c567d7d4725b398f7462a13170594a09` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/iqiyi/iqiyi/iqiyi.list) |
| singbox | `singbox/iqiyi/iqiyi/iqiyi.json` | 0 | 1992 | `aced68cbb6e419bfeca167cf5ed58ac1f0e042ac4444cc1730a3162f68f6f9a4` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/iqiyi/iqiyi/iqiyi.json) |
| surge | `surge/iqiyi/iqiyi/iqiyi.list` | 76 | 1953 | `247d0447bdad415f05924b96c617e077c567d7d4725b398f7462a13170594a09` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/iqiyi/iqiyi/iqiyi.list) |

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