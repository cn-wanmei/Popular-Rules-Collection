<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/adobe.png" alt="Adobe 图标" width="72" height="72">

# Adobe — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `adobe` |
| 类型 | provider_aggregate |
| Provider | `adobe` |
| 语义规则数量 | **140** |
| 语义 SHA-256 | `1bdf128c1a898dee0c1844bf56e0ea3038339ae395fbfa72fbccf60b91f5132a` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.adobe`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/adobe.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/adobe/adobe.yaml` | 140 | 3055 | `41bcf89b5b79e03b2bfa2949143fde8262250238f1445ab3ca9dc589bc5de414` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/adobe/adobe.yaml) |
| loon | `loon/adobe/adobe.list` | 140 | 4118 | `cfe6500c4bdd0916dcf5b53cb30f291bf7ea125d7c39591e2db66b875a806aff` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/adobe/adobe.list) |
| mihomo | `mihomo/adobe/adobe.yaml` | 140 | 4687 | `b04b3c9d86faef4f637de998f7384c8d097d9691736c47f41bee02f06b4ab0e9` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/adobe/adobe.yaml) |
| quantumultx | `quantumultx/adobe/adobe.list` | 140 | 4958 | `ea508c9c9fb2c73a6a9644c3822d2ab7f21cd631434c6b09bdbeb0a93c2b609b` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/adobe/adobe.list) |
| shadowrocket | `shadowrocket/adobe/adobe.list` | 140 | 4118 | `cfe6500c4bdd0916dcf5b53cb30f291bf7ea125d7c39591e2db66b875a806aff` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/adobe/adobe.list) |
| singbox | `singbox/adobe/adobe.json` | 0 | 3845 | `154ba02f6124b8b1e8314eb9f9be5acbd2f4f61c768e41b1be6e0808b9298725` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/adobe/adobe.json) |
| surge | `surge/adobe/adobe.list` | 140 | 4118 | `cfe6500c4bdd0916dcf5b53cb30f291bf7ea125d7c39591e2db66b875a806aff` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/adobe/adobe.list) |

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