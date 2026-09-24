<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/material-symbols/service.svg" alt="Sohu 图标" width="72" height="72">

# Sohu — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `sohu` |
| 类型 | service |
| Provider | `sohu` |
| 语义规则数量 | **53** |
| 语义 SHA-256 | `3e34b0b7ebfb1727e8ba044ea78f7887f6ac96107d1683ad90173ae49f820a62` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**material-symbols semantic fallback**

- Style：`material-symbols`
- Identity：`semantic.fallback.material-symbols`
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/material-symbols/service.svg`
- 该图标用于覆盖缺失身份，不代表官方品牌 Logo。

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/sohu/sohu/sohu.yaml` | 53 | 916 | `6b33a676b9aadf3034c2db7c3eb19f23d261a6ae11f0eb314740588ecda63157` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/sohu/sohu/sohu.yaml) |
| loon | `loon/sohu/sohu/sohu.list` | 53 | 1321 | `e7f2de6889125ab601f945c8ff02b295ae06e37056a6be64aa430cd20bacb748` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/sohu/sohu/sohu.list) |
| mihomo | `mihomo/sohu/sohu/sohu.yaml` | 53 | 1542 | `f43f4970780b326720da34b1e1d270964321194ca4b61836040f9a6237e2289d` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/sohu/sohu/sohu.yaml) |
| quantumultx | `quantumultx/sohu/sohu/sohu.list` | 53 | 1639 | `bf6a12278641a69a0180947b389e55320242bef64bc0c0c5300ca45d708a63dd` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/sohu/sohu/sohu.list) |
| shadowrocket | `shadowrocket/sohu/sohu/sohu.list` | 53 | 1321 | `e7f2de6889125ab601f945c8ff02b295ae06e37056a6be64aa430cd20bacb748` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/sohu/sohu/sohu.list) |
| singbox | `singbox/sohu/sohu/sohu.json` | 0 | 1243 | `ff0812db496a87f476163c50a603bd135c9954c4dc4f232f3da3f654f9c63e3e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/sohu/sohu/sohu.json) |
| surge | `surge/sohu/sohu/sohu.list` | 53 | 1321 | `e7f2de6889125ab601f945c8ff02b295ae06e37056a6be64aa430cd20bacb748` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/sohu/sohu/sohu.list) |

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