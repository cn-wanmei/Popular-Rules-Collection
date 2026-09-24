<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/amazon.png" alt="Amazon 图标" width="72" height="72">

# Amazon — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `amazon` |
| 类型 | provider_aggregate |
| Provider | `amazon` |
| 语义规则数量 | **305** |
| 语义 SHA-256 | `3e1f73b786c9f2884e4ff6d5b57cd02690ad2991c62238b2adbae785bc072e8b` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.amazon`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/amazon.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/amazon/amazon.yaml` | 303 | 6848 | `1e8a7d38f6a060f5f6a9a5d1841076668014e3f3cd6dc67d9c86f803e6c988e4` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/amazon/amazon.yaml) |
| loon | `loon/amazon/amazon.list` | 302 | 8913 | `1b1185eff1f71f2907f4b2424b7a950ee4be9327f73e14e82e0866e47cc5e35f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/amazon/amazon.list) |
| mihomo | `mihomo/amazon/amazon.yaml` | 303 | 10192 | `292e3b05713e1b2b3732e9cd064f9d50bffafb10f3b78552899272165755a683` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/amazon/amazon.yaml) |
| quantumultx | `quantumultx/amazon/amazon.list` | 302 | 10779 | `976e92e981a2793669866374b393207f50cddcd071c8ea1fac02d44c107287e9` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/amazon/amazon.list) |
| shadowrocket | `shadowrocket/amazon/amazon.list` | 302 | 8913 | `1b1185eff1f71f2907f4b2424b7a950ee4be9327f73e14e82e0866e47cc5e35f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/amazon/amazon.list) |
| singbox | `singbox/amazon/amazon.json` | 0 | 8467 | `4a2028da0c99cb033846a634f6b098fafaeaf08ff0e1daa585811e410b5e82e0` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/amazon/amazon.json) |
| surge | `surge/amazon/amazon.list` | 302 | 8913 | `1b1185eff1f71f2907f4b2424b7a950ee4be9327f73e14e82e0866e47cc5e35f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/amazon/amazon.list) |

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