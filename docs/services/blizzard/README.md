<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/material-symbols/service.svg" alt="Blizzard Entertainment 图标" width="72" height="72">

# Blizzard Entertainment — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `blizzard_aggregate` |
| 类型 | provider_aggregate |
| Provider | `blizzard` |
| 语义规则数量 | **62** |
| 语义 SHA-256 | `f008dd3e5d8586d3a4a8edb04dda7deb528b188cd9b42c6f4e8a222e19a2a2e8` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**material-symbols semantic fallback**

- Style：`material-symbols`
- Identity：`semantic.fallback.material-symbols`
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/material-symbols/service.svg`
- 该图标用于覆盖缺失身份，不代表官方品牌 Logo。

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/blizzard/blizzard.yaml` | 62 | 1552 | `860988e9b6c78bf4d0806959e08935792374c805af6ed0dda16a165ce8caaf7c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/blizzard/blizzard.yaml) |
| loon | `loon/blizzard/blizzard.list` | 62 | 1878 | `6ddd4778f0728ef5261b4609b5fbe3fb17c2cfedc4097f3003832063391fe80f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/blizzard/blizzard.list) |
| mihomo | `mihomo/blizzard/blizzard.yaml` | 62 | 2135 | `3f639462b312e2e3ce614d7167309067b5da4d2a89d8206fbfeb9e2e4da0123a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/blizzard/blizzard.yaml) |
| quantumultx | `quantumultx/blizzard/blizzard.list` | 62 | 2296 | `e3464331c99c31846f69ee1097ad5f134a5faa00afcbe53d316638f5fe3c34ed` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/blizzard/blizzard.list) |
| shadowrocket | `shadowrocket/blizzard/blizzard.list` | 62 | 1878 | `6ddd4778f0728ef5261b4609b5fbe3fb17c2cfedc4097f3003832063391fe80f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/blizzard/blizzard.list) |
| singbox | `singbox/blizzard/blizzard.json` | 0 | 1938 | `f25090a8dab624372445ccf5b1040c14b3fbc6cb772fa7df203d8a868f6644a1` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/blizzard/blizzard.json) |
| surge | `surge/blizzard/blizzard.list` | 62 | 1878 | `6ddd4778f0728ef5261b4609b5fbe3fb17c2cfedc4097f3003832063391fe80f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/blizzard/blizzard.list) |

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