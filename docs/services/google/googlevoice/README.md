<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/fluent/service.svg" alt="Google Voice 图标" width="72" height="72">

# Google Voice — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `googlevoice` |
| 类型 | service |
| Provider | `google` |
| 语义规则数量 | **1** |
| 语义 SHA-256 | `555b8533d71f542bb779effaea2f8e7f341e62744a37061173e295202c528a52` |
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
| egern | `egern/google/googlevoice/googlevoice.yaml` | 1 | 36 | `e18c9777c637cb12324cb508e87bb39bc6dfc2f715b486de7be57834490552fe` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/google/googlevoice/googlevoice.yaml) |
| loon | `loon/google/googlevoice/googlevoice.list` | 1 | 25 | `71aee9dfa0771f5d327d29bf9e0f1132c0819c5faa05ff3fe561f6987ee5a3c8` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/google/googlevoice/googlevoice.list) |
| mihomo | `mihomo/google/googlevoice/googlevoice.yaml` | 1 | 38 | `2336a3dc9d21717dc634e1523820a1c0daddc409225e195b82035d64c111c8ee` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/google/googlevoice/googlevoice.yaml) |
| quantumultx | `quantumultx/google/googlevoice/googlevoice.list` | 1 | 31 | `e5f4b7491a549842fc187e66badbf5d2d6a00256a6329177cb5b6a1a919028ae` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/google/googlevoice/googlevoice.list) |
| shadowrocket | `shadowrocket/google/googlevoice/googlevoice.list` | 1 | 25 | `71aee9dfa0771f5d327d29bf9e0f1132c0819c5faa05ff3fe561f6987ee5a3c8` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/google/googlevoice/googlevoice.list) |
| singbox | `singbox/google/googlevoice/googlevoice.json` | 0 | 103 | `9657318ec70a746221abd96b12daf6d006a4e9e0624d064e115d51ec29fd20de` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/google/googlevoice/googlevoice.json) |
| surge | `surge/google/googlevoice/googlevoice.list` | 1 | 25 | `71aee9dfa0771f5d327d29bf9e0f1132c0819c5faa05ff3fe561f6987ee5a3c8` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/google/googlevoice/googlevoice.list) |

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