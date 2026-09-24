<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/kakaotalk.png" alt="KakaoTalk 图标" width="72" height="72">

# KakaoTalk — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `kakaotalk_aggregate` |
| 类型 | provider_aggregate |
| Provider | `kakaotalk` |
| 语义规则数量 | **15** |
| 语义 SHA-256 | `9bec648e483638a32f7fd8db4c6fb5a9f795b11a70842f755d8dab22f9d687c3` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.kakaotalk`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/kakaotalk.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/kakaotalk/kakaotalk.yaml` | 15 | 327 | `6c2d2d313427d48b3db89b790798ee093373e608e501c1624dc8d80b46d0a3e9` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/kakaotalk/kakaotalk.yaml) |
| loon | `loon/kakaotalk/kakaotalk.list` | 15 | 379 | `98bab504849dee1177b423112173f9934486e1436076e1a3aa290b012c224c32` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/kakaotalk/kakaotalk.list) |
| mihomo | `mihomo/kakaotalk/kakaotalk.yaml` | 15 | 448 | `b9f44479ece9953ff8ed205e68c8bb1e3e50d784a275d5ee94027778cf5040e3` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/kakaotalk/kakaotalk.yaml) |
| quantumultx | `quantumultx/kakaotalk/kakaotalk.list` | 15 | 481 | `7ba278a6d261a1fa7576e5ca8ad1fcc738810da6bcb032a22378f793f225dc9b` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/kakaotalk/kakaotalk.list) |
| shadowrocket | `shadowrocket/kakaotalk/kakaotalk.list` | 15 | 379 | `98bab504849dee1177b423112173f9934486e1436076e1a3aa290b012c224c32` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/kakaotalk/kakaotalk.list) |
| singbox | `singbox/kakaotalk/kakaotalk.json` | 0 | 478 | `299d1ea18ac253b108d692508e2eb42b5de86b63ae600579f1b4429dca8c3a30` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/kakaotalk/kakaotalk.json) |
| surge | `surge/kakaotalk/kakaotalk.list` | 15 | 379 | `98bab504849dee1177b423112173f9934486e1436076e1a3aa290b012c224c32` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/kakaotalk/kakaotalk.list) |

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