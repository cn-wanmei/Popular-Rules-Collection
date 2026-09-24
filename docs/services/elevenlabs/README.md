<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/phosphor/service.svg" alt="ElevenLabs 图标" width="72" height="72">

# ElevenLabs — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `elevenlabs_aggregate` |
| 类型 | provider_aggregate |
| Provider | `elevenlabs` |
| 语义规则数量 | **2** |
| 语义 SHA-256 | `1b6866748729d5fc1d78e2bc4908658775c43dc348a0d885b6636113943449b4` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**phosphor semantic fallback**

- Style：`phosphor`
- Identity：`semantic.fallback.phosphor`
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/phosphor/service.svg`
- 该图标用于覆盖缺失身份，不代表官方品牌 Logo。

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/elevenlabs/elevenlabs.yaml` | 2 | 60 | `0afe7641b892b88413405c44d8b8b03f663cefe10d1ddd0d2071ab7deac8d192` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/elevenlabs/elevenlabs.yaml) |
| loon | `loon/elevenlabs/elevenlabs.list` | 2 | 57 | `42763bec3b93eadfd570a08593476302a2ae1a57aad578eff566a4b4a479950e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/elevenlabs/elevenlabs.list) |
| mihomo | `mihomo/elevenlabs/elevenlabs.yaml` | 2 | 74 | `62c5c3aeb9a088b64854c4eab09565a38f69135e4dbdee3541fc79f6f558b0af` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/elevenlabs/elevenlabs.yaml) |
| quantumultx | `quantumultx/elevenlabs/elevenlabs.list` | 2 | 69 | `0153cbaace43dd3a133969144acfed29591e04503e2a09105df09dd6966c3c86` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/elevenlabs/elevenlabs.list) |
| shadowrocket | `shadowrocket/elevenlabs/elevenlabs.list` | 2 | 57 | `42763bec3b93eadfd570a08593476302a2ae1a57aad578eff566a4b4a479950e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/elevenlabs/elevenlabs.list) |
| singbox | `singbox/elevenlabs/elevenlabs.json` | 0 | 132 | `5dad1e10662ab1b565d113bf68fefb8bbc6a67b00685d7989b0500684365767a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/elevenlabs/elevenlabs.json) |
| surge | `surge/elevenlabs/elevenlabs.list` | 2 | 57 | `42763bec3b93eadfd570a08593476302a2ae1a57aad578eff566a4b4a479950e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/elevenlabs/elevenlabs.list) |

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