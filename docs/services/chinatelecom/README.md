<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/chinatelecom.png" alt="China Telecom 图标" width="72" height="72">

# China Telecom — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `chinatelecom_aggregate` |
| 类型 | provider_aggregate |
| Provider | `chinatelecom` |
| 语义规则数量 | **83** |
| 语义 SHA-256 | `8905b9cfd34833b67959aafdeef76dab7f88a1aea6d0c00715901595f77d24e4` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`semantic.chinatelecom`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/chinatelecom.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/chinatelecom/chinatelecom.yaml` | 83 | 1527 | `f8cc6f2d305c033bf22a63039eb4f090fce044a916d2fe65c9809b00856ff1a6` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/chinatelecom/chinatelecom.yaml) |
| loon | `loon/chinatelecom/chinatelecom.list` | 83 | 2172 | `09e969677c3e87df0a72cd9588806f7b98281401d363ae867465cce85be9dfd4` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/chinatelecom/chinatelecom.list) |
| mihomo | `mihomo/chinatelecom/chinatelecom.yaml` | 83 | 2513 | `0d987a9d39eb9c261e142bb562715faebac9e618e1e23dc8e40f34ee538f5756` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/chinatelecom/chinatelecom.yaml) |
| quantumultx | `quantumultx/chinatelecom/chinatelecom.list` | 83 | 2670 | `10b370e65a5d7f0feeba5fbeb2139a1a6f473c1a330d71a5b6e292145fdb381d` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/chinatelecom/chinatelecom.list) |
| shadowrocket | `shadowrocket/chinatelecom/chinatelecom.list` | 83 | 2172 | `09e969677c3e87df0a72cd9588806f7b98281401d363ae867465cce85be9dfd4` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/chinatelecom/chinatelecom.list) |
| singbox | `singbox/chinatelecom/chinatelecom.json` | 0 | 2004 | `604ebbcbf192799641a81f5d1b89414ec9d6b5930e1bd6beacf81fe8355a10f5` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/chinatelecom/chinatelecom.json) |
| surge | `surge/chinatelecom/chinatelecom.list` | 83 | 2172 | `09e969677c3e87df0a72cd9588806f7b98281401d363ae867465cce85be9dfd4` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/chinatelecom/chinatelecom.list) |

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