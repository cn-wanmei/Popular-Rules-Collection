<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/bluesky.png" alt="Bluesky 图标" width="72" height="72">

# Bluesky — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `bluesky` |
| 类型 | service |
| Provider | `bluesky` |
| 语义规则数量 | **3** |
| 语义 SHA-256 | `b6d358f82d25894627ab82e837fec1685e0b62b17d48d7429eabaf6fb907cb0c` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.bluesky`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/bluesky.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/bluesky/bluesky/bluesky.yaml` | 3 | 71 | `bc2cb752f9f40fca97e2f039c17be95d0b3d8d91092498c202614e568819f041` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/bluesky/bluesky/bluesky.yaml) |
| loon | `loon/bluesky/bluesky/bluesky.list` | 3 | 76 | `88f76f0821993154a665c11cfeef25c4cd22a899d690d069adfc75b5c3248163` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/bluesky/bluesky/bluesky.list) |
| mihomo | `mihomo/bluesky/bluesky/bluesky.yaml` | 3 | 97 | `8c2fb427a50556d3bda957ca051c84a3e3c959e0a7cf5819360e5b9b81cad557` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/bluesky/bluesky/bluesky.yaml) |
| quantumultx | `quantumultx/bluesky/bluesky/bluesky.list` | 3 | 94 | `f08e4aaf50384d2b1ce3389116252e51e77fa2fffd1bec3e69db5f1e93067fa9` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/bluesky/bluesky/bluesky.list) |
| shadowrocket | `shadowrocket/bluesky/bluesky/bluesky.list` | 3 | 76 | `88f76f0821993154a665c11cfeef25c4cd22a899d690d069adfc75b5c3248163` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/bluesky/bluesky/bluesky.list) |
| singbox | `singbox/bluesky/bluesky/bluesky.json` | 0 | 148 | `4af050a3f44461bb5f1802a557e7da53ec45bf8f09d1c99f3fb33ec95c4a0677` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/bluesky/bluesky/bluesky.json) |
| surge | `surge/bluesky/bluesky/bluesky.list` | 3 | 76 | `88f76f0821993154a665c11cfeef25c4cd22a899d690d069adfc75b5c3248163` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/bluesky/bluesky/bluesky.list) |

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