<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/tabler/service.svg" alt="Microsoft Edge 图标" width="72" height="72">

# Microsoft Edge — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `microsoftedge` |
| 类型 | service |
| Provider | `microsoft` |
| 语义规则数量 | **4** |
| 语义 SHA-256 | `527849a37d404a10404ca5ef3f756374dbb1c9390a47d765537d9058d1b05c9f` |
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
| egern | `egern/microsoft/microsoftedge/microsoftedge.yaml` | 4 | 133 | `747af4c098f4d020045cf792850260b15816141126da90b441f94a204bd0a2bf` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/microsoft/microsoftedge/microsoftedge.yaml) |
| loon | `loon/microsoft/microsoftedge/microsoftedge.list` | 4 | 125 | `9775c3b021402322bfedecad925890b7be994bcf6706448bc010737c130af75c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/microsoft/microsoftedge/microsoftedge.list) |
| mihomo | `mihomo/microsoft/microsoftedge/microsoftedge.yaml` | 4 | 150 | `b74a4c79f3ac574db67fb509f803135e81d80fb1ca51260889e8a1184c827047` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/microsoft/microsoftedge/microsoftedge.yaml) |
| quantumultx | `quantumultx/microsoft/microsoftedge/microsoftedge.list` | 4 | 149 | `e7ad9bcaf098ea160685e3fc123b1907185f9e32e9dbaf35f1dc30bc414bcf6c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/microsoft/microsoftedge/microsoftedge.list) |
| shadowrocket | `shadowrocket/microsoft/microsoftedge/microsoftedge.list` | 4 | 125 | `9775c3b021402322bfedecad925890b7be994bcf6706448bc010737c130af75c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/microsoft/microsoftedge/microsoftedge.list) |
| singbox | `singbox/microsoft/microsoftedge/microsoftedge.json` | 0 | 215 | `b4f9d3db89c98fb7425e5c8deef224bb2dd496f0876602cf4669a185eec20bb7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/microsoft/microsoftedge/microsoftedge.json) |
| surge | `surge/microsoft/microsoftedge/microsoftedge.list` | 4 | 125 | `9775c3b021402322bfedecad925890b7be994bcf6706448bc010737c130af75c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/microsoft/microsoftedge/microsoftedge.list) |

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