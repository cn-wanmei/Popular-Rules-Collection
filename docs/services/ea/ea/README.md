<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/ea.png" alt="Electronic Arts 图标" width="72" height="72">

# Electronic Arts — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `ea` |
| 类型 | service |
| Provider | `ea` |
| 语义规则数量 | **165** |
| 语义 SHA-256 | `2712535ca558c2f5b36484ef3f47cb7e6b50fb75bba07373d2596e7c5f5eb5ff` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.ea`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/ea.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/ea/ea/ea.yaml` | 165 | 3868 | `70c078bfe725433a80091d1b5b3df9f8312579ddfea6dc4c59e2481a5354e251` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/ea/ea/ea.yaml) |
| loon | `loon/ea/ea/ea.list` | 165 | 5143 | `a95c849104a0cd99d433b340141b3d82bfa79ea7519424e7c44e4870c8447a07` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/ea/ea/ea.list) |
| mihomo | `mihomo/ea/ea/ea.yaml` | 165 | 5812 | `790092f1642aca2d68e7f5f81f24c76368306e1e82aa3bcc3ef3096ad9fba25e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/ea/ea/ea.yaml) |
| quantumultx | `quantumultx/ea/ea/ea.list` | 165 | 6133 | `7f3bcda01124bdb4462be1e78eecf586dd670cc0cbfa85a0438a2da9ed065ad8` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/ea/ea/ea.list) |
| shadowrocket | `shadowrocket/ea/ea/ea.list` | 165 | 5143 | `a95c849104a0cd99d433b340141b3d82bfa79ea7519424e7c44e4870c8447a07` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/ea/ea/ea.list) |
| singbox | `singbox/ea/ea/ea.json` | 0 | 4769 | `be334e4c791b670606e9ef6d2bc0214acdf227881edf886996593eb7b5d4abce` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/ea/ea/ea.json) |
| surge | `surge/ea/ea/ea.list` | 165 | 5143 | `a95c849104a0cd99d433b340141b3d82bfa79ea7519424e7c44e4870c8447a07` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/ea/ea/ea.list) |

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