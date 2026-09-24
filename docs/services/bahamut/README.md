<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/fluent/service.svg" alt="Bahamut 图标" width="72" height="72">

# Bahamut — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `bahamut_aggregate` |
| 类型 | provider_aggregate |
| Provider | `bahamut` |
| 语义规则数量 | **7** |
| 语义 SHA-256 | `bebf289f62a9369905ef56e3c7f6575879e91ddef38b2cf28ad21fb2b29262b7` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**fluent semantic fallback**

- Style：`fluent`
- Identity：`semantic.fallback.fluent`
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/fluent/service.svg`
- 该图标用于覆盖缺失身份，不代表官方品牌 Logo。

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/bahamut/bahamut.yaml` | 7 | 167 | `9e8f4cd2d2364055a81e21afc3e3be18d3f4aada47264ae7fb32777dd4932bef` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/bahamut/bahamut.yaml) |
| loon | `loon/bahamut/bahamut.list` | 7 | 185 | `82e06ddbe554ab8ee38a88d081b9f2c8ad06d8d6e603fe280adf2aa365727596` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/bahamut/bahamut.list) |
| mihomo | `mihomo/bahamut/bahamut.yaml` | 7 | 222 | `34b2e4dfd9e9d0805bfdc2de90d91c480d1a9aefc69313a0ef58ad6ca062712c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/bahamut/bahamut.yaml) |
| quantumultx | `quantumultx/bahamut/bahamut.list` | 7 | 227 | `3427882141701e9097f9bce96577cff8b6354c240bf6541ebd9f601a84a8bce0` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/bahamut/bahamut.list) |
| shadowrocket | `shadowrocket/bahamut/bahamut.list` | 7 | 185 | `82e06ddbe554ab8ee38a88d081b9f2c8ad06d8d6e603fe280adf2aa365727596` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/bahamut/bahamut.list) |
| singbox | `singbox/bahamut/bahamut.json` | 0 | 278 | `a03146258536603e5bdaa16e6b48d4399b4ba39c0fae93ef42e3d39c60e0613f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/bahamut/bahamut.json) |
| surge | `surge/bahamut/bahamut.list` | 7 | 185 | `82e06ddbe554ab8ee38a88d081b9f2c8ad06d8d6e603fe280adf2aa365727596` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/bahamut/bahamut.list) |

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