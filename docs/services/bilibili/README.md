<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/bilibili.png" alt="Bilibili 图标" width="72" height="72">

# Bilibili — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `bilibili_aggregate` |
| 类型 | provider_aggregate |
| Provider | `bilibili` |
| 语义规则数量 | **136** |
| 语义 SHA-256 | `f75f039a72a70f893893fd2b6caaf217e9ea8dddd1b1d866fd9c9dd621d169cb` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.bilibili`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/bilibili.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/bilibili/bilibili.yaml` | 130 | 3788 | `4810f3f81acb4f04f4cfc96952d33db8a7e4fb9d98847f35801d6082097062be` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/bilibili/bilibili.yaml) |
| loon | `loon/bilibili/bilibili.list` | 130 | 4351 | `26617b9c5abe13979c7be81bb439b74fb1cb143d1e2242e69cfb713120c44c35` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/bilibili/bilibili.list) |
| mihomo | `mihomo/bilibili/bilibili.yaml` | 130 | 4880 | `f4d860b1b410db8c8a6f09f8f43b6d9e20305f64884bd2783d1a0fb951460604` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/bilibili/bilibili.yaml) |
| quantumultx | `quantumultx/bilibili/bilibili.list` | 130 | 5147 | `875c8a5ffe4118879830aebffb6803c3fe7be538e5786ac39960f4d34832687e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/bilibili/bilibili.list) |
| shadowrocket | `shadowrocket/bilibili/bilibili.list` | 130 | 4351 | `26617b9c5abe13979c7be81bb439b74fb1cb143d1e2242e69cfb713120c44c35` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/bilibili/bilibili.list) |
| singbox | `singbox/bilibili/bilibili.json` | 0 | 4528 | `a020c2862fed563b9dcaab5787eb989aba71833b8ff4b2cae43589916170edb7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/bilibili/bilibili.json) |
| surge | `surge/bilibili/bilibili.list` | 130 | 4351 | `26617b9c5abe13979c7be81bb439b74fb1cb143d1e2242e69cfb713120c44c35` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/bilibili/bilibili.list) |

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