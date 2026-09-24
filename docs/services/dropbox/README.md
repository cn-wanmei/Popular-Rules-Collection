<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/dropbox.png" alt="Dropbox 图标" width="72" height="72">

# Dropbox — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `dropbox_aggregate` |
| 类型 | provider_aggregate |
| Provider | `dropbox` |
| 语义规则数量 | **17** |
| 语义 SHA-256 | `a702924b0eee94f5867e61f80a0053fc933ead37a88019e3edd49f41ac0292b7` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.dropbox`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/dropbox.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/dropbox/dropbox.yaml` | 17 | 424 | `a34a5e880fab128c577c61eea08c059a5922da664dd154c805bb2f912633bc8f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/dropbox/dropbox.yaml) |
| loon | `loon/dropbox/dropbox.list` | 17 | 541 | `028c59053d36eb2e51fcb5650ba1a9828f649ffd2e261cda2b1e81430a3a9e03` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/dropbox/dropbox.list) |
| mihomo | `mihomo/dropbox/dropbox.yaml` | 17 | 618 | `1e9bbbc3de8dea228f52fc5c7cd7f8a131443b3584608673d91c263933c0ca77` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/dropbox/dropbox.yaml) |
| quantumultx | `quantumultx/dropbox/dropbox.list` | 17 | 643 | `2bb4d5e8098b6d07d1323a9241d44108270d47ff24b527069b35285b5fcd7de8` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/dropbox/dropbox.list) |
| shadowrocket | `shadowrocket/dropbox/dropbox.list` | 17 | 541 | `028c59053d36eb2e51fcb5650ba1a9828f649ffd2e261cda2b1e81430a3a9e03` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/dropbox/dropbox.list) |
| singbox | `singbox/dropbox/dropbox.json` | 0 | 571 | `42395ec9ca2103f2932d1cc2c14f0fcbac3cddd0996d3298f3f93b0bd5eb4caa` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/dropbox/dropbox.json) |
| surge | `surge/dropbox/dropbox.list` | 17 | 541 | `028c59053d36eb2e51fcb5650ba1a9828f649ffd2e261cda2b1e81430a3a9e03` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/dropbox/dropbox.list) |

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