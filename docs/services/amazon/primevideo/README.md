<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/heroicons/service.svg" alt="Prime Video 图标" width="72" height="72">

# Prime Video — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `primevideo` |
| 类型 | service |
| Provider | `amazon` |
| 语义规则数量 | **26** |
| 语义 SHA-256 | `2778598d3839159f9e2f1a0f1b13867e985e3aca7f06cce40a0ff1cabe2f7c7d` |
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
| egern | `egern/amazon/primevideo/primevideo.yaml` | 25 | 677 | `1a0f43b21bca7fb01632a416806f1ee79661f4fefbf67b15f32451d4632bc568` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/amazon/primevideo/primevideo.yaml) |
| loon | `loon/amazon/primevideo/primevideo.list` | 25 | 792 | `1dc4d514a0fe48105efffe3de5a2468372d391b71db16b687392b270aab27439` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/amazon/primevideo/primevideo.list) |
| mihomo | `mihomo/amazon/primevideo/primevideo.yaml` | 25 | 901 | `e6102e4b6aabd2028945fb7b413d033982b960b07858f0405b0389c592d8477e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/amazon/primevideo/primevideo.yaml) |
| quantumultx | `quantumultx/amazon/primevideo/primevideo.list` | 25 | 942 | `77b1e6b80f17b01813b3d169a6e62942bcab3eb3753f85032b0cb2b112a23620` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/amazon/primevideo/primevideo.list) |
| shadowrocket | `shadowrocket/amazon/primevideo/primevideo.list` | 25 | 792 | `1dc4d514a0fe48105efffe3de5a2468372d391b71db16b687392b270aab27439` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/amazon/primevideo/primevideo.list) |
| singbox | `singbox/amazon/primevideo/primevideo.json` | 0 | 892 | `e41d6423d25b49f626eade660b94d5f73c29b7f8b4cc575372116945eb1cd9ba` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/amazon/primevideo/primevideo.json) |
| surge | `surge/amazon/primevideo/primevideo.list` | 25 | 792 | `1dc4d514a0fe48105efffe3de5a2468372d391b71db16b687392b270aab27439` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/amazon/primevideo/primevideo.list) |

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