<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/zhihu.png" alt="Zhihu 图标" width="72" height="72">

# Zhihu — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `zhihu_aggregate` |
| 类型 | provider_aggregate |
| Provider | `zhihu` |
| 语义规则数量 | **7** |
| 语义 SHA-256 | `77a2770739e1b4875791c580e7e487832b55d2eacc1abc4d68cd5ae1565c9b19` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.zhihu`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/zhihu.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/zhihu/zhihu.yaml` | 7 | 221 | `2133312e8471b7f97771afc45c42da4c876ccf44d6c5cd130e7f17e1b8a6f6ec` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/zhihu/zhihu.yaml) |
| loon | `loon/zhihu/zhihu.list` | 7 | 202 | `0f2aa3e5b20c08c7d6404bdf960a62713282465ed80e8cd5194e6874e6b57f8e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/zhihu/zhihu.list) |
| mihomo | `mihomo/zhihu/zhihu.yaml` | 7 | 239 | `dbf0ba01e24e37a08a6a12f406199ef1c44b18bccba550380a27ca449ca6704a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/zhihu/zhihu.yaml) |
| quantumultx | `quantumultx/zhihu/zhihu.list` | 7 | 254 | `6a30900af169d8e730219387ccff1d811478a27f04679c338639558d6cacfca1` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/zhihu/zhihu.list) |
| shadowrocket | `shadowrocket/zhihu/zhihu.list` | 7 | 202 | `0f2aa3e5b20c08c7d6404bdf960a62713282465ed80e8cd5194e6874e6b57f8e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/zhihu/zhihu.list) |
| singbox | `singbox/zhihu/zhihu.json` | 0 | 318 | `d37104b702ac50200082cd23ceeda910d9b48977597fe8e0eb16df30e5b876f3` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/zhihu/zhihu.json) |
| surge | `surge/zhihu/zhihu.list` | 7 | 202 | `0f2aa3e5b20c08c7d6404bdf960a62713282465ed80e8cd5194e6874e6b57f8e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/zhihu/zhihu.list) |

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