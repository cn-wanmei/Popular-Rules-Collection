<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/vercel.png" alt="Vercel 图标" width="72" height="72">

# Vercel — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `vercel` |
| 类型 | service |
| Provider | `vercel` |
| 语义规则数量 | **27** |
| 语义 SHA-256 | `b05758b97ee01304719bf91778de1fe3b1e35038fc1b5bdeeb68b79d8c1d5bb6` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.vercel`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/vercel.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/vercel/vercel/vercel.yaml` | 27 | 521 | `afb5cad0c10317b6966ef5f644631124e74bc2baf66cf4eb0e9565dbcd1ac27d` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/vercel/vercel/vercel.yaml) |
| loon | `loon/vercel/vercel/vercel.list` | 27 | 718 | `71981a03db63d8a0cddc2da54b228fe5b23d8270e8c199f9a7159a64aa933768` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/vercel/vercel/vercel.list) |
| mihomo | `mihomo/vercel/vercel/vercel.yaml` | 27 | 835 | `2acaa2f010080dfd67b167edf01115c25a019ef75fe53b39fba83a164436b8ca` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/vercel/vercel/vercel.yaml) |
| quantumultx | `quantumultx/vercel/vercel/vercel.list` | 27 | 880 | `c233af68244682d7f25691701a26be7c2e156d4917b0d6d879491300acb01b2a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/vercel/vercel/vercel.list) |
| shadowrocket | `shadowrocket/vercel/vercel/vercel.list` | 27 | 718 | `71981a03db63d8a0cddc2da54b228fe5b23d8270e8c199f9a7159a64aa933768` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/vercel/vercel/vercel.list) |
| singbox | `singbox/vercel/vercel/vercel.json` | 0 | 718 | `a9a17f72c2ccc517e8c403b6309210866dcd41bd41a593d8c0c5ad68435973fd` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/vercel/vercel/vercel.json) |
| surge | `surge/vercel/vercel/vercel.list` | 27 | 718 | `71981a03db63d8a0cddc2da54b228fe5b23d8270e8c199f9a7159a64aa933768` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/vercel/vercel/vercel.list) |

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