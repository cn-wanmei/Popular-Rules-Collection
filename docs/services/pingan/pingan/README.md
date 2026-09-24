<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/fluent/service.svg" alt="Ping An 图标" width="72" height="72">

# Ping An — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `pingan` |
| 类型 | service |
| Provider | `pingan` |
| 语义规则数量 | **27** |
| 语义 SHA-256 | `fe6a2b6d029369602eb5d8fd93d1f0c123d2fce1bb81640a2eca185f1eaa6179` |
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
| egern | `egern/pingan/pingan/pingan.yaml` | 27 | 540 | `66fec963bb623d2aeea96fed8f852c226174d0c129b6b7b2fc3e4716587fc737` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/pingan/pingan/pingan.yaml) |
| loon | `loon/pingan/pingan/pingan.list` | 27 | 737 | `9dfad52328d184592ee23855fa153752256b1ef8338b6a3f332440e090aa29e0` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/pingan/pingan/pingan.list) |
| mihomo | `mihomo/pingan/pingan/pingan.yaml` | 27 | 854 | `1f0e309010443bacab05593d2c47fb1440d779a87d8ad59f589e9c26511912d5` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/pingan/pingan/pingan.yaml) |
| quantumultx | `quantumultx/pingan/pingan/pingan.list` | 27 | 899 | `56b11ed07c1a4efcbfb922e0d8ac55e58d27d835de5e8417a822e736d9d29456` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/pingan/pingan/pingan.list) |
| shadowrocket | `shadowrocket/pingan/pingan/pingan.list` | 27 | 737 | `9dfad52328d184592ee23855fa153752256b1ef8338b6a3f332440e090aa29e0` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/pingan/pingan/pingan.list) |
| singbox | `singbox/pingan/pingan/pingan.json` | 0 | 737 | `90d7b22c384ca6d60ab397d49412577c7575853e44e8652eff182e9ce32b614e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/pingan/pingan/pingan.json) |
| surge | `surge/pingan/pingan/pingan.list` | 27 | 737 | `9dfad52328d184592ee23855fa153752256b1ef8338b6a3f332440e090aa29e0` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/pingan/pingan/pingan.list) |

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