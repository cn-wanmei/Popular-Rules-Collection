<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/lucide/service.svg" alt="KuGou 图标" width="72" height="72">

# KuGou — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `kugou` |
| 类型 | service |
| Provider | `kugou` |
| 语义规则数量 | **19** |
| 语义 SHA-256 | `204215d183beffa9bdd5f4b80b591a788d25a500356699b8eaf0bf01968a7451` |
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
| egern | `egern/kugou/kugou/kugou.yaml` | 19 | 422 | `0d0fb1a45d6acdd339e4822602781d44ff98af52db5f37433158ff7911cdf9bb` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/kugou/kugou/kugou.yaml) |
| loon | `loon/kugou/kugou/kugou.list` | 19 | 555 | `be52ef3ce4d615a4bfbfdf30ddf1f6d32f0465898507e84af457c1f8d6c4035e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/kugou/kugou/kugou.list) |
| mihomo | `mihomo/kugou/kugou/kugou.yaml` | 19 | 640 | `ae898a08b2c8acb3406985333142e369787fb3493dc670deb3e6155670e10f79` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/kugou/kugou/kugou.yaml) |
| quantumultx | `quantumultx/kugou/kugou/kugou.list` | 19 | 669 | `0f94fd7125aefc283aac175f0d75cc99e8997c89f0087c1c72fb404f5121b22b` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/kugou/kugou/kugou.list) |
| shadowrocket | `shadowrocket/kugou/kugou/kugou.list` | 19 | 555 | `be52ef3ce4d615a4bfbfdf30ddf1f6d32f0465898507e84af457c1f8d6c4035e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/kugou/kugou/kugou.list) |
| singbox | `singbox/kugou/kugou/kugou.json` | 0 | 579 | `0347bf82b93c6eb149d28f8bb20c128483cc591d054af56e234b092f5df4fae1` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/kugou/kugou/kugou.json) |
| surge | `surge/kugou/kugou/kugou.list` | 19 | 555 | `be52ef3ce4d615a4bfbfdf30ddf1f6d32f0465898507e84af457c1f8d6c4035e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/kugou/kugou/kugou.list) |

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