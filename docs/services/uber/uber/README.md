<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/uber.png" alt="Uber 图标" width="72" height="72">

# Uber — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `uber` |
| 类型 | service |
| Provider | `uber` |
| 语义规则数量 | **3** |
| 语义 SHA-256 | `be078ec6a2bcdf6707212dc6e91bcca77f638624bb3ed6bf4841b33ffa08b178` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.uber`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/uber.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/uber/uber/uber.yaml` | 6 | 131 | `f5069c6378925a8f2b9b53a020b25e6d5bce34d2c4149bf17626a40e772518fd` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/uber/uber/uber.yaml) |
| loon | `loon/uber/uber/uber.list` | 6 | 160 | `8ee247f00b04fbebad7cb28ca2a66c0a3f119c1b5f800d03dab0382e13ff2918` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/uber/uber/uber.list) |
| mihomo | `mihomo/uber/uber/uber.yaml` | 6 | 193 | `db815688b83947bae203f65200afb39267a48ae9ee12003b526a9386c2cc0425` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/uber/uber/uber.yaml) |
| quantumultx | `quantumultx/uber/uber/uber.list` | 6 | 196 | `e92339fcd9faf37e4ce851562898b82ba317033bf5f8d2dc2ff49519636ffc0a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/uber/uber/uber.list) |
| shadowrocket | `shadowrocket/uber/uber/uber.list` | 6 | 160 | `8ee247f00b04fbebad7cb28ca2a66c0a3f119c1b5f800d03dab0382e13ff2918` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/uber/uber/uber.list) |
| singbox | `singbox/uber/uber/uber.json` | 0 | 223 | `512d4fcd758a2749a173341d9db73336258c724a28f8a767de3f978d17c5a6d1` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/uber/uber/uber.json) |
| surge | `surge/uber/uber/uber.list` | 6 | 160 | `8ee247f00b04fbebad7cb28ca2a66c0a3f119c1b5f800d03dab0382e13ff2918` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/uber/uber/uber.list) |

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