<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/airbnb.png" alt="Airbnb 图标" width="72" height="72">

# Airbnb — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `airbnb_aggregate` |
| 类型 | provider_aggregate |
| Provider | `airbnb` |
| 语义规则数量 | **83** |
| 语义 SHA-256 | `16a2bb3a0cbad36218e7e760e3f0b8a241855f158eb41badcba6d60844f1d19c` |
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
| egern | `egern/airbnb/airbnb.yaml` | 83 | 1499 | `d83a1d0e1358e3a983ea11e257261838330f37ca60927dcf2d49b27dbb295e22` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/airbnb/airbnb.yaml) |
| loon | `loon/airbnb/airbnb.list` | 83 | 2144 | `86f0fa2f798dbb7010b5883a5ed20e33e3b43151e138dc22c3a0e2cc002e2d3c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/airbnb/airbnb.list) |
| mihomo | `mihomo/airbnb/airbnb.yaml` | 83 | 2485 | `de30a0ec22805b4a4d86b31ad03d951ee53e6f3788250e571226fb9c5660f3c0` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/airbnb/airbnb.yaml) |
| quantumultx | `quantumultx/airbnb/airbnb.list` | 83 | 2642 | `b37916c83716f9d77d01bb43723e8aef6a24f75769245af4cd75ce50bd98e696` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/airbnb/airbnb.list) |
| shadowrocket | `shadowrocket/airbnb/airbnb.list` | 83 | 2144 | `86f0fa2f798dbb7010b5883a5ed20e33e3b43151e138dc22c3a0e2cc002e2d3c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/airbnb/airbnb.list) |
| singbox | `singbox/airbnb/airbnb.json` | 0 | 1976 | `1e82140d9a842f62aa555dd626fb73731ef34994bd6499a3baacbf2768741824` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/airbnb/airbnb.json) |
| surge | `surge/airbnb/airbnb.list` | 83 | 2144 | `86f0fa2f798dbb7010b5883a5ed20e33e3b43151e138dc22c3a0e2cc002e2d3c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/airbnb/airbnb.list) |

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