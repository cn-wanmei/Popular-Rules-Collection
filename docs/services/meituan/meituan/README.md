<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/meituan.png" alt="Meituan 图标" width="72" height="72">

# Meituan — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `meituan` |
| 类型 | service |
| Provider | `meituan` |
| 语义规则数量 | **7** |
| 语义 SHA-256 | `93a2ed0c1688f8023823e3a9209b6b565640bd7d275dc3582c788cb7164b5c38` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.meituan`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/meituan.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/meituan/meituan/meituan.yaml` | 7 | 141 | `96dc4a1fc5cde54d791d7c25b8fd71e4c88f5a9cc361e5723299fedc0cda2b30` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/meituan/meituan/meituan.yaml) |
| loon | `loon/meituan/meituan/meituan.list` | 7 | 178 | `6abcbfd2fcf6c66b14750242936b30cebf34fa074bb34676074b1a566a61fb50` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/meituan/meituan/meituan.list) |
| mihomo | `mihomo/meituan/meituan/meituan.yaml` | 7 | 215 | `d6fb670cd0a1437ee1db9bbde74ed64d052e22347f7b71a2e7a8addf13cfe1c1` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/meituan/meituan/meituan.yaml) |
| quantumultx | `quantumultx/meituan/meituan/meituan.list` | 7 | 220 | `1ab9524693df192fe7864e4d83d7c7a676c1e20384763b8b68e312ffed5210d2` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/meituan/meituan/meituan.list) |
| shadowrocket | `shadowrocket/meituan/meituan/meituan.list` | 7 | 178 | `6abcbfd2fcf6c66b14750242936b30cebf34fa074bb34676074b1a566a61fb50` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/meituan/meituan/meituan.list) |
| singbox | `singbox/meituan/meituan/meituan.json` | 0 | 238 | `bd97d19b771b9fd03c121166e9ea4ad35dbb43bb4a77bf54692cb6b702c3af7a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/meituan/meituan/meituan.json) |
| surge | `surge/meituan/meituan/meituan.list` | 7 | 178 | `6abcbfd2fcf6c66b14750242936b30cebf34fa074bb34676074b1a566a61fb50` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/meituan/meituan/meituan.list) |

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