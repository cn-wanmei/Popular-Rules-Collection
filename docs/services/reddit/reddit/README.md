<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/reddit.png" alt="Reddit 图标" width="72" height="72">

# Reddit — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `reddit` |
| 类型 | service |
| Provider | `reddit` |
| 语义规则数量 | **15** |
| 语义 SHA-256 | `866a91d1f8af211fad9845a1ae9dd1945bbcd96a7cb3c0eb7fe04de4bfec1310` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.reddit`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/reddit.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/reddit/reddit/reddit.yaml` | 32 | 734 | `62055abae0085fae4ecbe0e41f8358c5a5e41da15f08812232d66d0b5177df7e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/reddit/reddit/reddit.yaml) |
| loon | `loon/reddit/reddit/reddit.list` | 32 | 971 | `065fdf7d15bd5ef44f42e9d2dc370df4d6489224e2c7ac2e85c2f870ad896a12` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/reddit/reddit/reddit.list) |
| mihomo | `mihomo/reddit/reddit/reddit.yaml` | 32 | 1108 | `16bc045e2bec1c133502884e3b975adc9a12134c58095726b8359dfc16250e4b` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/reddit/reddit/reddit.yaml) |
| quantumultx | `quantumultx/reddit/reddit/reddit.list` | 32 | 1163 | `658f292722c5e637aa879914420e33d38b5004ceba2cc263eb22a8fabcc2a945` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/reddit/reddit/reddit.list) |
| shadowrocket | `shadowrocket/reddit/reddit/reddit.list` | 32 | 971 | `065fdf7d15bd5ef44f42e9d2dc370df4d6489224e2c7ac2e85c2f870ad896a12` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/reddit/reddit/reddit.list) |
| singbox | `singbox/reddit/reddit/reddit.json` | 0 | 956 | `aba67c1ad1d9e53ca1786db82e7cec8eb42b42e4f395837e4302cd9f1c14b448` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/reddit/reddit/reddit.json) |
| surge | `surge/reddit/reddit/reddit.list` | 32 | 971 | `065fdf7d15bd5ef44f42e9d2dc370df4d6489224e2c7ac2e85c2f870ad896a12` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/reddit/reddit/reddit.list) |

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