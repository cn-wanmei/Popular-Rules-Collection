<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/qqmusic.png" alt="QQ Music 图标" width="72" height="72">

# QQ Music — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `qqmusic` |
| 类型 | service |
| Provider | `tencent` |
| 语义规则数量 | **1** |
| 语义 SHA-256 | `288b35d8433fbbb790dff34a9421a05321e196b2379f62e4f8a38ef757b0a511` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.qqmusic`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/qqmusic.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/tencent/qqmusic/qqmusic.yaml` | 1 | 34 | `198c644efd0fd9b20a960bdc86dcb58e5345ebec76b21a986a798afe9e5ed080` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/tencent/qqmusic/qqmusic.yaml) |
| loon | `loon/tencent/qqmusic/qqmusic.list` | 1 | 23 | `568aaa426b7b09eb16eca124050239c135e1fc783a9b60c47522e6bc06bd5be8` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/tencent/qqmusic/qqmusic.list) |
| mihomo | `mihomo/tencent/qqmusic/qqmusic.yaml` | 1 | 36 | `8ce1ffbbbeedb90a9c6262e063a9d5a4f0123e5dbce9ce378733f5a8ae8c1278` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/tencent/qqmusic/qqmusic.yaml) |
| quantumultx | `quantumultx/tencent/qqmusic/qqmusic.list` | 1 | 29 | `f2c542439ad61e06fd10dbfbba3e4ae6682002ecce6864b02a5b2911920e2d6d` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/tencent/qqmusic/qqmusic.list) |
| shadowrocket | `shadowrocket/tencent/qqmusic/qqmusic.list` | 1 | 23 | `568aaa426b7b09eb16eca124050239c135e1fc783a9b60c47522e6bc06bd5be8` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/tencent/qqmusic/qqmusic.list) |
| singbox | `singbox/tencent/qqmusic/qqmusic.json` | 0 | 101 | `47ada722e7ccfd18e66983ec763f9da1426dfc7483c2562bd3e6c074acd32cfb` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/tencent/qqmusic/qqmusic.json) |
| surge | `surge/tencent/qqmusic/qqmusic.list` | 1 | 23 | `568aaa426b7b09eb16eca124050239c135e1fc783a9b60c47522e6bc06bd5be8` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/tencent/qqmusic/qqmusic.list) |

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