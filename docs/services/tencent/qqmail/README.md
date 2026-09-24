<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/qqmail.png" alt="QQ Mail 图标" width="72" height="72">

# QQ Mail — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `qqmail` |
| 类型 | service |
| Provider | `tencent` |
| 语义规则数量 | **1** |
| 语义 SHA-256 | `c85353f1a9c2b0c61cc170981b8f2430ee16edfff9309c0adff1d642892647c4` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.qqmail`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/qqmail.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/tencent/qqmail/qqmail.yaml` | 1 | 37 | `581d7bf6cab04332acdd2de04a57786e2a4dab9d964f5413a9a29e4eedfc3c2d` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/tencent/qqmail/qqmail.yaml) |
| loon | `loon/tencent/qqmail/qqmail.list` | 1 | 26 | `975c15d1a6282e72e4dd3ae20f4477c06e84450a1101bd976d6d6554a7bbaf14` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/tencent/qqmail/qqmail.list) |
| mihomo | `mihomo/tencent/qqmail/qqmail.yaml` | 1 | 39 | `8f3b7bb14c81bd45036c03494a9193fecead4ee7f65de72120e997a50e238899` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/tencent/qqmail/qqmail.yaml) |
| quantumultx | `quantumultx/tencent/qqmail/qqmail.list` | 1 | 32 | `1e4e44c2b1d2ce8d0d55d2d2b47d26af9996c7f058902b6cb9b67670fa84dee7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/tencent/qqmail/qqmail.list) |
| shadowrocket | `shadowrocket/tencent/qqmail/qqmail.list` | 1 | 26 | `975c15d1a6282e72e4dd3ae20f4477c06e84450a1101bd976d6d6554a7bbaf14` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/tencent/qqmail/qqmail.list) |
| singbox | `singbox/tencent/qqmail/qqmail.json` | 0 | 104 | `2938ddd973f934a7e652b9a0c7679b99bc2c5299afd5f547e443e412183354bf` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/tencent/qqmail/qqmail.json) |
| surge | `surge/tencent/qqmail/qqmail.list` | 1 | 26 | `975c15d1a6282e72e4dd3ae20f4477c06e84450a1101bd976d6d6554a7bbaf14` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/tencent/qqmail/qqmail.list) |

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