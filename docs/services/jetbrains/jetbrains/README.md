<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/jetbrains.png" alt="JetBrains 图标" width="72" height="72">

# JetBrains — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `jetbrains` |
| 类型 | service |
| Provider | `jetbrains` |
| 语义规则数量 | **25** |
| 语义 SHA-256 | `4149136fe79d24d2fd7e8bfca2c769696cc947cec1b1729f6de9977309a264d1` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.jetbrains`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/jetbrains.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/jetbrains/jetbrains/jetbrains.yaml` | 36 | 728 | `64fc00fbec2f21e6862c94a39b81858b65782f1e94310ea92db263121e7c1399` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/jetbrains/jetbrains/jetbrains.yaml) |
| loon | `loon/jetbrains/jetbrains/jetbrains.list` | 36 | 997 | `86a813d217bad6c61fbdad7eb75dec15d2bc8e74242c42b4414aef7abfa196c2` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/jetbrains/jetbrains/jetbrains.list) |
| mihomo | `mihomo/jetbrains/jetbrains/jetbrains.yaml` | 36 | 1150 | `b5524d336bd4094a2129f28ed39a0f39c93ac306b498b1e39678e5a0b7581c5b` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/jetbrains/jetbrains/jetbrains.yaml) |
| quantumultx | `quantumultx/jetbrains/jetbrains/jetbrains.list` | 36 | 1213 | `8049d48af307b3f0c380badfb8ff976a5245d58a37852e0984cf4103afee7458` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/jetbrains/jetbrains/jetbrains.list) |
| shadowrocket | `shadowrocket/jetbrains/jetbrains/jetbrains.list` | 36 | 997 | `86a813d217bad6c61fbdad7eb75dec15d2bc8e74242c42b4414aef7abfa196c2` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/jetbrains/jetbrains/jetbrains.list) |
| singbox | `singbox/jetbrains/jetbrains/jetbrains.json` | 0 | 970 | `bd937e913b0c4e43f6b2c8662b001f69dafaa3cf63f45f99651805ab57a3b094` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/jetbrains/jetbrains/jetbrains.json) |
| surge | `surge/jetbrains/jetbrains/jetbrains.list` | 36 | 997 | `86a813d217bad6c61fbdad7eb75dec15d2bc8e74242c42b4414aef7abfa196c2` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/jetbrains/jetbrains/jetbrains.list) |

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