<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/nintendo.png" alt="Nintendo 图标" width="72" height="72">

# Nintendo — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `nintendo_aggregate` |
| 类型 | provider_aggregate |
| Provider | `nintendo` |
| 语义规则数量 | **126** |
| 语义 SHA-256 | `f0584713412c1e8a104000296c19f3ccda67abccd8b76534f1cb4c56afb749eb` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.nintendo`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/nintendo.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/nintendo/nintendo.yaml` | 126 | 2965 | `64fcdb2f7baa435f460fbbc6f4d20612bd823b9238e2cff96856ba7dbd73dd86` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/nintendo/nintendo.yaml) |
| loon | `loon/nintendo/nintendo.list` | 126 | 3935 | `408efb35076a8058201637b7f29a0f0de3694f7219d6cd1ecfec6ad1056b8c57` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/nintendo/nintendo.list) |
| mihomo | `mihomo/nintendo/nintendo.yaml` | 126 | 4448 | `8105809345581d5b8604ed347e80a403115bcb4a01e72cabc88c566e08ed16ef` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/nintendo/nintendo.yaml) |
| quantumultx | `quantumultx/nintendo/nintendo.list` | 126 | 4693 | `bebdb987fa4cdc045a50207f7b95e2b8fdac02874d12d931740c2af70a3c9f14` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/nintendo/nintendo.list) |
| shadowrocket | `shadowrocket/nintendo/nintendo.list` | 126 | 3935 | `408efb35076a8058201637b7f29a0f0de3694f7219d6cd1ecfec6ad1056b8c57` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/nintendo/nintendo.list) |
| singbox | `singbox/nintendo/nintendo.json` | 0 | 3671 | `4998c7adf3911b94ddbc888a547b84da6a19faebfc644ff912436ec0aa375411` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/nintendo/nintendo.json) |
| surge | `surge/nintendo/nintendo.list` | 126 | 3935 | `408efb35076a8058201637b7f29a0f0de3694f7219d6cd1ecfec6ad1056b8c57` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/nintendo/nintendo.list) |

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