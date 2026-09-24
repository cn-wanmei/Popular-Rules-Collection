<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/huawei.png" alt="Huawei 图标" width="72" height="72">

# Huawei — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `huawei` |
| 类型 | provider_aggregate |
| Provider | `huawei` |
| 语义规则数量 | **402** |
| 语义 SHA-256 | `6fbd85e945c6f6f2d1e956e3a0534af358e5e736d5ff2df42e767814916ebca3` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.huawei`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/huawei.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/huawei/huawei.yaml` | 402 | 8899 | `fcca26c070a04c394ab3383d0939402d64ae5b5f737d23d9b60aad545a581a0f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/huawei/huawei.yaml) |
| loon | `loon/huawei/huawei.list` | 402 | 12096 | `ff0118db6673896b8d88570ef8a36427087b77953be3d16a6ec53b38033af232` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/huawei/huawei.list) |
| mihomo | `mihomo/huawei/huawei.yaml` | 402 | 13713 | `f7b649709e5e74982f60b5b9afa76c6fc77bfddae0f1b7e6bf3c1e81563c3f36` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/huawei/huawei.yaml) |
| quantumultx | `quantumultx/huawei/huawei.list` | 402 | 14508 | `f3459fe3d337f67b434cc68b837f86768e56e63d47459d9f0c3da4b6c9cc9b61` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/huawei/huawei.list) |
| shadowrocket | `shadowrocket/huawei/huawei.list` | 402 | 12096 | `ff0118db6673896b8d88570ef8a36427087b77953be3d16a6ec53b38033af232` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/huawei/huawei.list) |
| singbox | `singbox/huawei/huawei.json` | 0 | 10971 | `8e682a6881ac7f69832a27b1cd6f1556a84835bf1496aa1f54d6c071a0a3ad2d` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/huawei/huawei.json) |
| surge | `surge/huawei/huawei.list` | 402 | 12096 | `ff0118db6673896b8d88570ef8a36427087b77953be3d16a6ec53b38033af232` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/huawei/huawei.list) |

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