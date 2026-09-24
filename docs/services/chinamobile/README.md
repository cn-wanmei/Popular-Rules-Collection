<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/chinamobile.png" alt="China Mobile 图标" width="72" height="72">

# China Mobile — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `chinamobile_aggregate` |
| 类型 | provider_aggregate |
| Provider | `chinamobile` |
| 语义规则数量 | **38** |
| 语义 SHA-256 | `5b3b653d7ed6e63afa1653d581c38e98729d3f4956a53ec9021a449537c021c5` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`semantic.chinamobile`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/chinamobile.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/chinamobile/chinamobile.yaml` | 38 | 735 | `98e591e707046ba63ef1ae361ad34f44df5a165f16f8f92392d3e05dc39af893` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/chinamobile/chinamobile.yaml) |
| loon | `loon/chinamobile/chinamobile.list` | 38 | 1001 | `be232aacdb8d1cb70d0264e1d91c6e0de5d5c78a8d906aa5710fc79d2f546733` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/chinamobile/chinamobile.list) |
| mihomo | `mihomo/chinamobile/chinamobile.yaml` | 38 | 1162 | `d7c8f536c574c620ca031a875d51b560b0b5e8ad2b5bb4ffd5ff4c53e91ac4b0` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/chinamobile/chinamobile.yaml) |
| quantumultx | `quantumultx/chinamobile/chinamobile.list` | 38 | 1231 | `22f41d3c67342ab635e927bdd8787cb957952901c54bd581a72a7c0d6c67e360` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/chinamobile/chinamobile.list) |
| shadowrocket | `shadowrocket/chinamobile/chinamobile.list` | 38 | 1001 | `be232aacdb8d1cb70d0264e1d91c6e0de5d5c78a8d906aa5710fc79d2f546733` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/chinamobile/chinamobile.list) |
| singbox | `singbox/chinamobile/chinamobile.json` | 0 | 1001 | `7a9606eee6d4d9981b95e4e1e548942aa2d2b69e484972e503121f2460df368f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/chinamobile/chinamobile.json) |
| surge | `surge/chinamobile/chinamobile.list` | 38 | 1001 | `be232aacdb8d1cb70d0264e1d91c6e0de5d5c78a8d906aa5710fc79d2f546733` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/chinamobile/chinamobile.list) |

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