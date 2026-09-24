<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/tabler/service.svg" alt="Trip.com 图标" width="72" height="72">

# Trip.com — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `ctrip_aggregate` |
| 类型 | provider_aggregate |
| Provider | `ctrip` |
| 语义规则数量 | **29** |
| 语义 SHA-256 | `164f299cd9a07f484e8379c65c5c18df9523c2e28110e9bb515c082725a96a57` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**tabler semantic fallback**

- Style：`tabler`
- Identity：`semantic.fallback.tabler`
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/tabler/service.svg`
- 该图标用于覆盖缺失身份，不代表官方品牌 Logo。

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/ctrip/ctrip.yaml` | 29 | 532 | `5eb9674d7ddafc47c93947533c486212d72469632f9693d9bbc701c10568abf0` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/ctrip/ctrip.yaml) |
| loon | `loon/ctrip/ctrip.list` | 29 | 745 | `c4fb6008957fcf86eec90a36ff6cdf06ae6de4cfc96535ab090c7e6df6d781e9` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/ctrip/ctrip.list) |
| mihomo | `mihomo/ctrip/ctrip.yaml` | 29 | 870 | `19057ea6cca2ab89f0256526fd9b6e62919b06bd366d281af869d9e0688b390a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/ctrip/ctrip.yaml) |
| quantumultx | `quantumultx/ctrip/ctrip.list` | 29 | 919 | `eaf7e52ecdec02f970d0a4f1f9e19eb43d6da1adb2525bf435ecbf31d99ba18e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/ctrip/ctrip.list) |
| shadowrocket | `shadowrocket/ctrip/ctrip.list` | 29 | 745 | `c4fb6008957fcf86eec90a36ff6cdf06ae6de4cfc96535ab090c7e6df6d781e9` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/ctrip/ctrip.list) |
| singbox | `singbox/ctrip/ctrip.json` | 0 | 739 | `fd18a1e6f8dd43d45b957b6496adeff3af861dc4c1458db4a60fb5554e1f0f0b` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/ctrip/ctrip.json) |
| surge | `surge/ctrip/ctrip.list` | 29 | 745 | `c4fb6008957fcf86eec90a36ff6cdf06ae6de4cfc96535ab090c7e6df6d781e9` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/ctrip/ctrip.list) |

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