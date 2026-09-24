<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/solar/service.svg" alt="Snap 图标" width="72" height="72">

# Snap — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `snap` |
| 类型 | provider_aggregate |
| Provider | `snap` |
| 语义规则数量 | **9** |
| 语义 SHA-256 | `2cb5a5aac5210de364dc07dc0a9989e58df3caf9561431f180ed3c5a523e1210` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**solar semantic fallback**

- Style：`solar`
- Identity：`semantic.fallback.solar`
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/solar/service.svg`
- 该图标用于覆盖缺失身份，不代表官方品牌 Logo。

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/snap/snap.yaml` | 9 | 207 | `d60fccc89839adbbf28e2e2562d22487892e6b858cbbf2a91e05b72b65266c75` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/snap/snap.yaml) |
| loon | `loon/snap/snap.list` | 9 | 260 | `f34547b7febbe94f4fecea57ceb4dffd00a204f5ffd2ef20c99fe85f46dd7a4a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/snap/snap.list) |
| mihomo | `mihomo/snap/snap.yaml` | 9 | 305 | `0169cc3f2cbb9d646d2f29ddd37176ce84b82fb92aeffc9773188f403d863f13` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/snap/snap.yaml) |
| quantumultx | `quantumultx/snap/snap.list` | 9 | 314 | `11bf728add1fcfb95f3b35938657945970ce4170f468b20e88d3b4578d69c306` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/snap/snap.list) |
| shadowrocket | `shadowrocket/snap/snap.list` | 9 | 260 | `f34547b7febbe94f4fecea57ceb4dffd00a204f5ffd2ef20c99fe85f46dd7a4a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/snap/snap.list) |
| singbox | `singbox/snap/snap.json` | 0 | 314 | `15671983edd3eae248ca01c2b8f3de254bb3ed440c5313142e0b9711e0e7e965` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/snap/snap.json) |
| surge | `surge/snap/snap.list` | 9 | 260 | `f34547b7febbe94f4fecea57ceb4dffd00a204f5ffd2ef20c99fe85f46dd7a4a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/snap/snap.list) |

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