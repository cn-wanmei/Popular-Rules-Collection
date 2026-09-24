<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/lucide/service.svg" alt="DiDi 图标" width="72" height="72">

# DiDi — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `didi_aggregate` |
| 类型 | provider_aggregate |
| Provider | `didi` |
| 语义规则数量 | **25** |
| 语义 SHA-256 | `a5efd882caed82bb46bf5b285e91437d36fa9f878be6dc2436009e11a141958b` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**lucide semantic fallback**

- Style：`lucide`
- Identity：`semantic.fallback.lucide`
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/lucide/service.svg`
- 该图标用于覆盖缺失身份，不代表官方品牌 Logo。

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/didi/didi.yaml` | 25 | 527 | `81a4e87870c090b6da6236bb189dd3e5136a8b3448cb234e89521ff42af1cd54` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/didi/didi.yaml) |
| loon | `loon/didi/didi.list` | 25 | 708 | `bfde8c97a4408bb174a94190f63e356f0a815e3d636758985eb2bbf761c20751` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/didi/didi.list) |
| mihomo | `mihomo/didi/didi.yaml` | 25 | 817 | `8cbfe3b305b23d5ec4b21adaea6d91b0a5b118e85100e01762da0567c571608e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/didi/didi.yaml) |
| quantumultx | `quantumultx/didi/didi.list` | 25 | 858 | `66b868da9d0d16f6fc024c4b1aa813dacae7d1a36c3087dec2339e93011a13fa` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/didi/didi.list) |
| shadowrocket | `shadowrocket/didi/didi.list` | 25 | 708 | `bfde8c97a4408bb174a94190f63e356f0a815e3d636758985eb2bbf761c20751` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/didi/didi.list) |
| singbox | `singbox/didi/didi.json` | 0 | 714 | `41d317bbd8ba492936c45ecd23f8140f9a31238837dfdbf2dc6c6f6543a1da72` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/didi/didi.json) |
| surge | `surge/didi/didi.list` | 25 | 708 | `bfde8c97a4408bb174a94190f63e356f0a815e3d636758985eb2bbf761c20751` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/didi/didi.list) |

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