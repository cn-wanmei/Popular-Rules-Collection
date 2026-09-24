<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/playstation.png" alt="PlayStation 图标" width="72" height="72">

# PlayStation — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `playstation_aggregate` |
| 类型 | provider_aggregate |
| Provider | `playstation` |
| 语义规则数量 | **4** |
| 语义 SHA-256 | `de65c3bd1e3ae32c49594e678fd4d74e30eb8192d25b1c3d04f40ec4d74dc74f` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.playstation`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/playstation.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/playstation/playstation.yaml` | 4 | 127 | `5ac773a71acf81b06f410388d1140803484c73f35391f8dd132d471f82990c22` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/playstation/playstation.yaml) |
| loon | `loon/playstation/playstation.list` | 4 | 140 | `487ad286b1b0a8c7664831d3e1a4e66e2e4144907924e4ec580d735f6991e6de` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/playstation/playstation.list) |
| mihomo | `mihomo/playstation/playstation.yaml` | 4 | 165 | `ccdfaaa25a6ca56cd89b74516e472257685826b6bb93d8dd52d7345c0d24ec2e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/playstation/playstation.yaml) |
| quantumultx | `quantumultx/playstation/playstation.list` | 4 | 164 | `51e0f309ca2e05484267c3d5f5bdfca43230fa1e76c4e972fc5de2aa84eac7eb` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/playstation/playstation.list) |
| shadowrocket | `shadowrocket/playstation/playstation.list` | 4 | 140 | `487ad286b1b0a8c7664831d3e1a4e66e2e4144907924e4ec580d735f6991e6de` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/playstation/playstation.list) |
| singbox | `singbox/playstation/playstation.json` | 0 | 209 | `4f4fdca7f2d937d137e121213b809916d58b251bc6d75a69f5c0b59d2e736a31` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/playstation/playstation.json) |
| surge | `surge/playstation/playstation.list` | 4 | 140 | `487ad286b1b0a8c7664831d3e1a4e66e2e4144907924e4ec580d735f6991e6de` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/playstation/playstation.list) |

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