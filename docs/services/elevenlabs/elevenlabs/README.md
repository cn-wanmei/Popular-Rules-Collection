<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/fluent/service.svg" alt="ElevenLabs 图标" width="72" height="72">

# ElevenLabs — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `elevenlabs` |
| 类型 | service |
| Provider | `elevenlabs` |
| 语义规则数量 | **2** |
| 语义 SHA-256 | `c7f48548a2b07593718f8ecc1ab52eaa8e1ac519b0a005a80c8793541544d47d` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**fluent semantic fallback**

- Style：`fluent`
- Identity：`semantic.fallback.fluent`
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/fluent/service.svg`
- 该图标用于覆盖缺失身份，不代表官方品牌 Logo。

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/elevenlabs/elevenlabs/elevenlabs.yaml` | 4 | 101 | `d4d299033b7236c8df2278cb8b01223902bc3de03ecb74305bde645635c38da6` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/elevenlabs/elevenlabs/elevenlabs.yaml) |
| loon | `loon/elevenlabs/elevenlabs/elevenlabs.list` | 4 | 114 | `5a6d0cb85a39ce8a9f4df7cad21f76a8af74769fce6b98a9ed2e1345a5409f1d` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/elevenlabs/elevenlabs/elevenlabs.list) |
| mihomo | `mihomo/elevenlabs/elevenlabs/elevenlabs.yaml` | 4 | 139 | `bfa1e402851e01614e19e1ca4e0c548febf2982c31da96675ad96b05c47a4813` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/elevenlabs/elevenlabs/elevenlabs.yaml) |
| quantumultx | `quantumultx/elevenlabs/elevenlabs/elevenlabs.list` | 4 | 138 | `b1299a3f8d4573284006d6112d0b988a481e4d810b61065f7cc513529a3232d6` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/elevenlabs/elevenlabs/elevenlabs.list) |
| shadowrocket | `shadowrocket/elevenlabs/elevenlabs/elevenlabs.list` | 4 | 114 | `5a6d0cb85a39ce8a9f4df7cad21f76a8af74769fce6b98a9ed2e1345a5409f1d` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/elevenlabs/elevenlabs/elevenlabs.list) |
| singbox | `singbox/elevenlabs/elevenlabs/elevenlabs.json` | 0 | 183 | `b24919754e18230a5b9ac298d0e6af7f9d1c6867cef85ad1e5de2ab9f10a279a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/elevenlabs/elevenlabs/elevenlabs.json) |
| surge | `surge/elevenlabs/elevenlabs/elevenlabs.list` | 4 | 114 | `5a6d0cb85a39ce8a9f4df7cad21f76a8af74769fce6b98a9ed2e1345a5409f1d` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/elevenlabs/elevenlabs/elevenlabs.list) |

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