<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/remix/service.svg" alt="Trip.com 图标" width="72" height="72">

# Trip.com — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `ctrip` |
| 类型 | service |
| Provider | `ctrip` |
| 语义规则数量 | **29** |
| 语义 SHA-256 | `a2db7f7c5f554f6dce66f7ed3d48d2d1b8bd51be863a5c2f19bf93846c16af63` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**remix semantic fallback**

- Style：`remix`
- Identity：`semantic.fallback.remix`
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/remix/service.svg`
- 该图标用于覆盖缺失身份，不代表官方品牌 Logo。

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/ctrip/ctrip/ctrip.yaml` | 29 | 532 | `fd9923959b5e10b0448b3e298cb25e407004b77b7b46054da8914cfe9f9fe97d` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/ctrip/ctrip/ctrip.yaml) |
| loon | `loon/ctrip/ctrip/ctrip.list` | 29 | 745 | `c3d7e2594ae4fa10a4e65342fac7f25b3ab355a8d407598efe9e14e14ea9982c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/ctrip/ctrip/ctrip.list) |
| mihomo | `mihomo/ctrip/ctrip/ctrip.yaml` | 29 | 870 | `d775d7fbd08aead2b23bfbfe326b4428a3a191c9deb8bb672da810f1f3624b1b` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/ctrip/ctrip/ctrip.yaml) |
| quantumultx | `quantumultx/ctrip/ctrip/ctrip.list` | 29 | 919 | `7830e882e0ce87d9361143a05481c04317de30e465bbe1e0fba834120bc7af40` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/ctrip/ctrip/ctrip.list) |
| shadowrocket | `shadowrocket/ctrip/ctrip/ctrip.list` | 29 | 745 | `c3d7e2594ae4fa10a4e65342fac7f25b3ab355a8d407598efe9e14e14ea9982c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/ctrip/ctrip/ctrip.list) |
| singbox | `singbox/ctrip/ctrip/ctrip.json` | 0 | 739 | `a195ce0898984b890b3b18111bc0864701a56028b23faf327f7d6c27b0e2cd69` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/ctrip/ctrip/ctrip.json) |
| surge | `surge/ctrip/ctrip/ctrip.list` | 29 | 745 | `c3d7e2594ae4fa10a4e65342fac7f25b3ab355a8d407598efe9e14e14ea9982c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/ctrip/ctrip/ctrip.list) |

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