<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/oppo.png" alt="OPPO 图标" width="72" height="72">

# OPPO — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `oppo_aggregate` |
| 类型 | provider_aggregate |
| Provider | `oppo` |
| 语义规则数量 | **56** |
| 语义 SHA-256 | `8efe8e148c5de0806d31dc4b924a405007f66156d817ddfa10781a0eb9a1ad7e` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.oppo`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/oppo.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/oppo/oppo.yaml` | 56 | 1076 | `1612fcaafd4f94248bdb97782c2644d2b685fe41bd3fb4f37bcebf58e978030c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/oppo/oppo.yaml) |
| loon | `loon/oppo/oppo.list` | 56 | 1505 | `fb122e28c637f719a435d7207b54740065e5e4f1aa9b775b94014153308d4a0c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/oppo/oppo.list) |
| mihomo | `mihomo/oppo/oppo.yaml` | 56 | 1738 | `ad8f3b9090fa5e6cbcfb0395a65a3f9ea8fd7c38a9b7cb9ee6053ed48002a4de` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/oppo/oppo.yaml) |
| quantumultx | `quantumultx/oppo/oppo.list` | 56 | 1841 | `7f84e5bab5486cd3483aa3720fb2e2edf0321bac39763fc326bac872bf30754f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/oppo/oppo.list) |
| shadowrocket | `shadowrocket/oppo/oppo.list` | 56 | 1505 | `fb122e28c637f719a435d7207b54740065e5e4f1aa9b775b94014153308d4a0c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/oppo/oppo.list) |
| singbox | `singbox/oppo/oppo.json` | 0 | 1418 | `1e912dcb99e87fea57679a7b777d2fd2d322f4c9e3111df68ba080b83bfaef4f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/oppo/oppo.json) |
| surge | `surge/oppo/oppo.list` | 56 | 1505 | `fb122e28c637f719a435d7207b54740065e5e4f1aa9b775b94014153308d4a0c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/oppo/oppo.list) |

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