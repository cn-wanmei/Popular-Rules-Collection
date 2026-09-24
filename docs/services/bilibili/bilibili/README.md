<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/bilibili.png" alt="Bilibili 图标" width="72" height="72">

# Bilibili — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `bilibili` |
| 类型 | service |
| Provider | `bilibili` |
| 语义规则数量 | **136** |
| 语义 SHA-256 | `5815c1ff22883d50c684a3a3f39a2e05b66590bdea95e258d96803861951b3a3` |
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
| egern | `egern/bilibili/bilibili/bilibili.yaml` | 220 | 5436 | `f74c4ee1c6629fa2e57c2c536aa44e222b69d7d99bde8e190fb27aa750ba37d9` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/bilibili/bilibili/bilibili.yaml) |
| loon | `loon/bilibili/bilibili/bilibili.list` | 220 | 6719 | `eede101aaf3a29ed0b8b7e6090abb1fa3894d345b87fa7f7b06dc954d2930d9e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/bilibili/bilibili/bilibili.list) |
| mihomo | `mihomo/bilibili/bilibili/bilibili.yaml` | 220 | 7608 | `ba802fc1a37445afc9effaf8540484bdb39efcbf87095356b5188e7a583dd883` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/bilibili/bilibili/bilibili.yaml) |
| quantumultx | `quantumultx/bilibili/bilibili/bilibili.list` | 220 | 8055 | `6a92a874bae4bb8a7d6efaf55a0b628f76f75c220490b943810da9aff9a94dfa` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/bilibili/bilibili/bilibili.list) |
| shadowrocket | `shadowrocket/bilibili/bilibili/bilibili.list` | 220 | 6719 | `eede101aaf3a29ed0b8b7e6090abb1fa3894d345b87fa7f7b06dc954d2930d9e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/bilibili/bilibili/bilibili.list) |
| singbox | `singbox/bilibili/bilibili/bilibili.json` | 0 | 6626 | `297dc483c09facde1e9896e610df07b9deb2e28a28c2a29ffa7552952e001597` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/bilibili/bilibili/bilibili.json) |
| surge | `surge/bilibili/bilibili/bilibili.list` | 220 | 6719 | `eede101aaf3a29ed0b8b7e6090abb1fa3894d345b87fa7f7b06dc954d2930d9e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/bilibili/bilibili/bilibili.list) |

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