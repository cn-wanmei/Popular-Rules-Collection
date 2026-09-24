<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/airbnb.png" alt="Airbnb 图标" width="72" height="72">

# Airbnb — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `airbnb` |
| 类型 | service |
| Provider | `airbnb` |
| 语义规则数量 | **83** |
| 语义 SHA-256 | `c8530262050f940a951cd46ce8b7c4b6f37bf2024087c04e40749b60e47fde75` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.airbnb`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/airbnb.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/airbnb/airbnb/airbnb.yaml` | 166 | 2979 | `600b85a179b87b461031216c5f616ba8fa5c5ef565c39579edf74b6458525da3` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/airbnb/airbnb/airbnb.yaml) |
| loon | `loon/airbnb/airbnb/airbnb.list` | 166 | 4288 | `e22be8813371530ec7c04bc44fba44cb7a8e808bc444a2230864e8253af1344a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/airbnb/airbnb/airbnb.list) |
| mihomo | `mihomo/airbnb/airbnb/airbnb.yaml` | 166 | 4961 | `ff34c88faffc8c1a1f057cfd3eee45321fb67568e8f1dac72add2b90f0e7a2ee` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/airbnb/airbnb/airbnb.yaml) |
| quantumultx | `quantumultx/airbnb/airbnb/airbnb.list` | 166 | 5284 | `6c728ab56f7cf8f834455a955003cf14ad9c0124469cfc2c9ae30067231f5dfc` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/airbnb/airbnb/airbnb.list) |
| shadowrocket | `shadowrocket/airbnb/airbnb/airbnb.list` | 166 | 4288 | `e22be8813371530ec7c04bc44fba44cb7a8e808bc444a2230864e8253af1344a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/airbnb/airbnb/airbnb.list) |
| singbox | `singbox/airbnb/airbnb/airbnb.json` | 0 | 3871 | `83c290fb37b264f517be86e4c88f01af23de4edd2ca992bec692531aeb24209e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/airbnb/airbnb/airbnb.json) |
| surge | `surge/airbnb/airbnb/airbnb.list` | 166 | 4288 | `e22be8813371530ec7c04bc44fba44cb7a8e808bc444a2230864e8253af1344a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/airbnb/airbnb/airbnb.list) |

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