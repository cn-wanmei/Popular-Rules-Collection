<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/weibo.png" alt="Weibo 图标" width="72" height="72">

# Weibo — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `weibo` |
| 类型 | service |
| Provider | `weibo` |
| 语义规则数量 | **4** |
| 语义 SHA-256 | `4613f8784a64b05b8f974f12e60ecb5bba46410e6322795418c826bfd85f2d3d` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.weibo`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/weibo.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/weibo/weibo/weibo.yaml` | 4 | 101 | `ae0d37bf6da0c26547f35fd304dab67c954c780e4fecb0d45b4d4188a1051c50` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/weibo/weibo/weibo.yaml) |
| loon | `loon/weibo/weibo/weibo.list` | 4 | 95 | `195eb35b72e9b6ac9ffabe7b9c98105b3dec936b722ec5b478e7401c62ecb0d7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/weibo/weibo/weibo.list) |
| mihomo | `mihomo/weibo/weibo/weibo.yaml` | 4 | 120 | `844d513346fb18f630532cee1caaeffd92cf1ed6acfe51683448a0f892414826` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/weibo/weibo/weibo.yaml) |
| quantumultx | `quantumultx/weibo/weibo/weibo.list` | 4 | 119 | `792fb119f551cae7b3e403dafbe0320da4cdd19fedc16c954058558f2f4f8a93` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/weibo/weibo/weibo.list) |
| shadowrocket | `shadowrocket/weibo/weibo/weibo.list` | 4 | 95 | `195eb35b72e9b6ac9ffabe7b9c98105b3dec936b722ec5b478e7401c62ecb0d7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/weibo/weibo/weibo.list) |
| singbox | `singbox/weibo/weibo/weibo.json` | 0 | 197 | `423f16434ce1f64bec9cc3abb9c4d0da2dea90ce8f748143ba340ce35e10f898` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/weibo/weibo/weibo.json) |
| surge | `surge/weibo/weibo/weibo.list` | 4 | 95 | `195eb35b72e9b6ac9ffabe7b9c98105b3dec936b722ec5b478e7401c62ecb0d7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/weibo/weibo/weibo.list) |

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