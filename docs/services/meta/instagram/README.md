<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/instagram.png" alt="Instagram 图标" width="72" height="72">

# Instagram — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `instagram` |
| 类型 | service |
| Provider | `meta` |
| 语义规则数量 | **76** |
| 语义 SHA-256 | `d732fd7badcf0ef2e45036bcfac4195d64e2cc2be0dfa89a555056747a2b7055` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.instagram`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/instagram.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/meta/instagram/instagram.yaml` | 152 | 3603 | `f0dd559405a8578a2b37058e134be8aee9edf5d8b7d9d2953662967e43e7ac6c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/meta/instagram/instagram.yaml) |
| loon | `loon/meta/instagram/instagram.list` | 152 | 4781 | `7b2b7eee3d4c08cc3e4218e10f837f3277d3432c057718892a735ce77565d947` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/meta/instagram/instagram.list) |
| mihomo | `mihomo/meta/instagram/instagram.yaml` | 152 | 5398 | `1f19019b5d97f506a5131757bca55d323596c87f7fa44d0b6e8faaada34f0153` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/meta/instagram/instagram.yaml) |
| quantumultx | `quantumultx/meta/instagram/instagram.list` | 152 | 5693 | `7e4515f15a8849b8600944e70e5432a6bb6f0942240a2ff39cc766b7126be61f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/meta/instagram/instagram.list) |
| shadowrocket | `shadowrocket/meta/instagram/instagram.list` | 152 | 4781 | `7b2b7eee3d4c08cc3e4218e10f837f3277d3432c057718892a735ce77565d947` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/meta/instagram/instagram.list) |
| singbox | `singbox/meta/instagram/instagram.json` | 0 | 4439 | `6dfc1a315a5d7c5bb1d6e0c838253c54a8e01552868de1e3cb3b337493f4633d` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/meta/instagram/instagram.json) |
| surge | `surge/meta/instagram/instagram.list` | 152 | 4781 | `7b2b7eee3d4c08cc3e4218e10f837f3277d3432c057718892a735ce77565d947` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/meta/instagram/instagram.list) |

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