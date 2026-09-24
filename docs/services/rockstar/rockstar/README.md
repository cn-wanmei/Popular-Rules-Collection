<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/rockstar.png" alt="Rockstar Games 图标" width="72" height="72">

# Rockstar Games — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `rockstar` |
| 类型 | service |
| Provider | `rockstar` |
| 语义规则数量 | **5** |
| 语义 SHA-256 | `708070e42915e30662bf6ed5cb1db12dc67df8dc842af96d881063aa66d4398a` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.rockstar`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/rockstar.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/rockstar/rockstar/rockstar.yaml` | 5 | 197 | `50b7adfefb8a3126cc1c81d52d72550749855da64e42569336cbd979d5c0d4d7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/rockstar/rockstar/rockstar.yaml) |
| loon | `loon/rockstar/rockstar/rockstar.list` | 5 | 218 | `eaed1e732a3df831d9adec608c1104dc3045e323a100b01b848ee6c0233f4a55` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/rockstar/rockstar/rockstar.list) |
| mihomo | `mihomo/rockstar/rockstar/rockstar.yaml` | 5 | 247 | `65b2f9464815f9127eb89ba83fce914109efbf0fe64deca25b065fb6a4c7cb60` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/rockstar/rockstar/rockstar.yaml) |
| quantumultx | `quantumultx/rockstar/rockstar/rockstar.list` | 5 | 248 | `288376f16c1d6b7d918548dd1a1859af7b19697e7004a9057aaa32d1900ae9b1` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/rockstar/rockstar/rockstar.list) |
| shadowrocket | `shadowrocket/rockstar/rockstar/rockstar.list` | 5 | 218 | `eaed1e732a3df831d9adec608c1104dc3045e323a100b01b848ee6c0233f4a55` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/rockstar/rockstar/rockstar.list) |
| singbox | `singbox/rockstar/rockstar/rockstar.json` | 0 | 284 | `adad07b3c6568dfabf4dcfb956387ae82f560fe66cbbf8be75db3e84859224e2` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/rockstar/rockstar/rockstar.json) |
| surge | `surge/rockstar/rockstar/rockstar.list` | 5 | 218 | `eaed1e732a3df831d9adec608c1104dc3045e323a100b01b848ee6c0233f4a55` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/rockstar/rockstar/rockstar.list) |

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