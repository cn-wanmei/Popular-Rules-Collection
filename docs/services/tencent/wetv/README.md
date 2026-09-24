<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/fluent/service.svg" alt="WeTV 图标" width="72" height="72">

# WeTV — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `wetv` |
| 类型 | service |
| Provider | `tencent` |
| 语义规则数量 | **9** |
| 语义 SHA-256 | `f4f183a35d0de5563a6cabe56ae00e1992375ca7d20e7933b221625ce67279f1` |
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
| egern | `egern/tencent/wetv/wetv.yaml` | 7 | 190 | `c7d6aaa69f54e0782ce9e80edd755742512601c6b098a9ddc3151695e9c7f3d5` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/tencent/wetv/wetv.yaml) |
| loon | `loon/tencent/wetv/wetv.list` | 7 | 189 | `a0d8d5a7b40411a37f02eaaba55390e55a425c0fd19f5112c675208d6a49b312` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/tencent/wetv/wetv.list) |
| mihomo | `mihomo/tencent/wetv/wetv.yaml` | 7 | 226 | `2457062ffb10247218804d557f6235c92f47b9f6dbc8b193911b165d67f04708` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/tencent/wetv/wetv.yaml) |
| quantumultx | `quantumultx/tencent/wetv/wetv.list` | 7 | 233 | `b9aaea9f9389518ad2e887d8a3dad7f3360895aca93281bfcb66197985238669` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/tencent/wetv/wetv.list) |
| shadowrocket | `shadowrocket/tencent/wetv/wetv.list` | 7 | 189 | `a0d8d5a7b40411a37f02eaaba55390e55a425c0fd19f5112c675208d6a49b312` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/tencent/wetv/wetv.list) |
| singbox | `singbox/tencent/wetv/wetv.json` | 0 | 315 | `84a55cb8e1462ce6bb9c13f61dd36ef3fe2968d1c0c13df9267a685ff54e3b7c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/tencent/wetv/wetv.json) |
| surge | `surge/tencent/wetv/wetv.list` | 7 | 189 | `a0d8d5a7b40411a37f02eaaba55390e55a425c0fd19f5112c675208d6a49b312` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/tencent/wetv/wetv.list) |

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