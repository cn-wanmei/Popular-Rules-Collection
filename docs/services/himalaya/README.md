<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/heroicons/service.svg" alt="Himalaya 图标" width="72" height="72">

# Himalaya — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `himalaya_aggregate` |
| 类型 | provider_aggregate |
| Provider | `himalaya` |
| 语义规则数量 | **17** |
| 语义 SHA-256 | `37ad204bc644172ee1626adbb8f5a2703e3ba7908f0dc2fbb0e6aff37fa10b3d` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**heroicons semantic fallback**

- Style：`heroicons`
- Identity：`semantic.fallback.heroicons`
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/heroicons/service.svg`
- 该图标用于覆盖缺失身份，不代表官方品牌 Logo。

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/himalaya/himalaya.yaml` | 17 | 340 | `27881f2f60ca9f832a204b8ab12f33a040b936a3db7bddca278ce797878f9e3f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/himalaya/himalaya.yaml) |
| loon | `loon/himalaya/himalaya.list` | 17 | 457 | `e34c85ffe825cccb7b5a705a1d0a735d8084cd5c61bdc09d8b355c64655238a7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/himalaya/himalaya.list) |
| mihomo | `mihomo/himalaya/himalaya.yaml` | 17 | 534 | `27a422735622cafe9f6b7456895946a619f16a04957c5d8a5937585ec6038ef6` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/himalaya/himalaya.yaml) |
| quantumultx | `quantumultx/himalaya/himalaya.list` | 17 | 559 | `ee680cd439788e7c5177d8f85ec7ca591d0201b63a23ebba5277924081934434` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/himalaya/himalaya.list) |
| shadowrocket | `shadowrocket/himalaya/himalaya.list` | 17 | 457 | `e34c85ffe825cccb7b5a705a1d0a735d8084cd5c61bdc09d8b355c64655238a7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/himalaya/himalaya.list) |
| singbox | `singbox/himalaya/himalaya.json` | 0 | 487 | `32c08c36fd6ff9103218e19a0a257c1e3e9635f628b550dc8ad26aa6a6e6104c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/himalaya/himalaya.json) |
| surge | `surge/himalaya/himalaya.list` | 17 | 457 | `e34c85ffe825cccb7b5a705a1d0a735d8084cd5c61bdc09d8b355c64655238a7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/himalaya/himalaya.list) |

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