<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/cainiao.png" alt="Cainiao 图标" width="72" height="72">

# Cainiao — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `cainiao` |
| 类型 | service |
| Provider | `alibaba` |
| 语义规则数量 | **1** |
| 语义 SHA-256 | `8fb83ea298e5493a448cc146c6fcdb5d5b8d992240c30f99175d919bccf3221d` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.cainiao`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/cainiao.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/alibaba/cainiao/cainiao.yaml` | 1 | 41 | `6aff07e899492dab7f5d5e9917ec90996a66379f222b22ead6796c9390cbd82c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/alibaba/cainiao/cainiao.yaml) |
| loon | `loon/alibaba/cainiao/cainiao.list` | 1 | 30 | `6158afb61abcd82e7bcfc80ae97700ffd0fdad2398221989eb4114598b1dd682` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/alibaba/cainiao/cainiao.list) |
| mihomo | `mihomo/alibaba/cainiao/cainiao.yaml` | 1 | 43 | `407b948bb2f4037c95a8db5c0270e4589e1adda400a7d2f4821094d4054c2d9d` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/alibaba/cainiao/cainiao.yaml) |
| quantumultx | `quantumultx/alibaba/cainiao/cainiao.list` | 1 | 36 | `0ff7d8db3c15c45175af3c4abdb86003addb34ae957e1563af5eb1ce7a53f51a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/alibaba/cainiao/cainiao.list) |
| shadowrocket | `shadowrocket/alibaba/cainiao/cainiao.list` | 1 | 30 | `6158afb61abcd82e7bcfc80ae97700ffd0fdad2398221989eb4114598b1dd682` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/alibaba/cainiao/cainiao.list) |
| singbox | `singbox/alibaba/cainiao/cainiao.json` | 0 | 108 | `93aa5dcdd70365b3bfba4f5a37c545826652b5020c78a9c1973526ec55f38096` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/alibaba/cainiao/cainiao.json) |
| surge | `surge/alibaba/cainiao/cainiao.list` | 1 | 30 | `6158afb61abcd82e7bcfc80ae97700ffd0fdad2398221989eb4114598b1dd682` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/alibaba/cainiao/cainiao.list) |

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