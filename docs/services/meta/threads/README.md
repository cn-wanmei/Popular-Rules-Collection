<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/threads.png" alt="Threads 图标" width="72" height="72">

# Threads — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `threads` |
| 类型 | service |
| Provider | `meta` |
| 语义规则数量 | **1** |
| 语义 SHA-256 | `31367a8ae44c8809b1dcff201685e8083a2032a1db056838fc853554cb4eebbd` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.threads`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/threads.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/meta/threads/threads.yaml` | 1 | 37 | `b7dc3f65fd3f545b37756828d8031efd0cb48d901bcb2cb685984b651f076fec` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/meta/threads/threads.yaml) |
| loon | `loon/meta/threads/threads.list` | 1 | 26 | `ca40554fbc0734376a911bec5498ca97591694d5383c30ce51042a9e8a099045` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/meta/threads/threads.list) |
| mihomo | `mihomo/meta/threads/threads.yaml` | 1 | 39 | `c46c027da29bd3cd29b5b2aa6d63a5810d96e0529ef837c86865bac6c5812b3a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/meta/threads/threads.yaml) |
| quantumultx | `quantumultx/meta/threads/threads.list` | 1 | 32 | `2cd44ac939ffb662baeee402aed91710d52bbec316f1933725df8e942cf5c94c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/meta/threads/threads.list) |
| shadowrocket | `shadowrocket/meta/threads/threads.list` | 1 | 26 | `ca40554fbc0734376a911bec5498ca97591694d5383c30ce51042a9e8a099045` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/meta/threads/threads.list) |
| singbox | `singbox/meta/threads/threads.json` | 0 | 104 | `2bfe361a7064edac1291f80c8aab1a5129ccdd97e4eb9be445bd643feeb34c7d` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/meta/threads/threads.json) |
| surge | `surge/meta/threads/threads.list` | 1 | 26 | `ca40554fbc0734376a911bec5498ca97591694d5383c30ce51042a9e8a099045` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/meta/threads/threads.list) |

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