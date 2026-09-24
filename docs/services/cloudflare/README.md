<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/cloudflare.png" alt="Cloudflare 图标" width="72" height="72">

# Cloudflare — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `cloudflare` |
| 类型 | provider_aggregate |
| Provider | `cloudflare` |
| 语义规则数量 | **98** |
| 语义 SHA-256 | `4d3cbb1a8e0ba731b7d79c1b90c6a37d308d8a587e09e96e2d69df39d9ddcf35` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.cloudflare`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/cloudflare.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/cloudflare/cloudflare.yaml` | 98 | 2307 | `e08b65375b7dc494c9f82f7e85c54be790a12998a54b92f22af3f30c4f05dde5` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/cloudflare/cloudflare.yaml) |
| loon | `loon/cloudflare/cloudflare.list` | 98 | 2920 | `e7d45de73cbec3aeb2e50cc768a938413bb049968661555abf346d75ab54163a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/cloudflare/cloudflare.list) |
| mihomo | `mihomo/cloudflare/cloudflare.yaml` | 98 | 3321 | `cbed116454ccb6c19418744441b19ff7826d2fe4f19031116a39309de06065ef` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/cloudflare/cloudflare.yaml) |
| quantumultx | `quantumultx/cloudflare/cloudflare.list` | 98 | 3552 | `38c654c361e0d911f3bc093983161379cc324b4268c37cc4f4c42ef03c86c94a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/cloudflare/cloudflare.list) |
| shadowrocket | `shadowrocket/cloudflare/cloudflare.list` | 98 | 2920 | `e7d45de73cbec3aeb2e50cc768a938413bb049968661555abf346d75ab54163a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/cloudflare/cloudflare.list) |
| singbox | `singbox/cloudflare/cloudflare.json` | 0 | 2859 | `f9f3ffcedbde83b9e30ed845866d43b27fb19139958e6a13407ad0da42093e70` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/cloudflare/cloudflare.json) |
| surge | `surge/cloudflare/cloudflare.list` | 98 | 2920 | `e7d45de73cbec3aeb2e50cc768a938413bb049968661555abf346d75ab54163a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/cloudflare/cloudflare.list) |

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