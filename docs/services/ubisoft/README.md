<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/ubisoft.png" alt="Ubisoft 图标" width="72" height="72">

# Ubisoft — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `ubisoft_aggregate` |
| 类型 | provider_aggregate |
| Provider | `ubisoft` |
| 语义规则数量 | **1** |
| 语义 SHA-256 | `66ece476e5bdfb6d790df153ee765f756862299823ae20e50bff0959f0dcf2b2` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.ubisoft`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/ubisoft.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/ubisoft/ubisoft.yaml` | 1 | 48 | `d53debeee18ec2ad5457ecf4c32abe942ec09b3e9ed57fecf3df53b8dee397eb` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/ubisoft/ubisoft.yaml) |
| loon | `loon/ubisoft/ubisoft.list` | 1 | 37 | `ded562bb0a0dbbc9f6512e796839ca255b463bfb1cfe5d7490f235dc7d507f04` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/ubisoft/ubisoft.list) |
| mihomo | `mihomo/ubisoft/ubisoft.yaml` | 1 | 50 | `15b563d7018a813d26fa266bc158402d64fd0a29517b37128d2d916be8951c59` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/ubisoft/ubisoft.yaml) |
| quantumultx | `quantumultx/ubisoft/ubisoft.list` | 1 | 43 | `7026b3fc036e388069ac1658f8edfe481b7b636b5d02f049dc2ded15f03fc5cf` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/ubisoft/ubisoft.list) |
| shadowrocket | `shadowrocket/ubisoft/ubisoft.list` | 1 | 37 | `ded562bb0a0dbbc9f6512e796839ca255b463bfb1cfe5d7490f235dc7d507f04` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/ubisoft/ubisoft.list) |
| singbox | `singbox/ubisoft/ubisoft.json` | 0 | 115 | `0441c3fc3b1107828242e69b4db3327342694e46aa24ada84544c1221aed517d` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/ubisoft/ubisoft.json) |
| surge | `surge/ubisoft/ubisoft.list` | 1 | 37 | `ded562bb0a0dbbc9f6512e796839ca255b463bfb1cfe5d7490f235dc7d507f04` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/ubisoft/ubisoft.list) |

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