<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/tidal.png" alt="TIDAL 图标" width="72" height="72">

# TIDAL — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `tidal` |
| 类型 | service |
| Provider | `tidal` |
| 语义规则数量 | **3** |
| 语义 SHA-256 | `f024c04e891a20d6f65c93e8b1c3e27bc5627815f2751bf862cd32a21e889951` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.tidal`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/tidal.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/tidal/tidal/tidal.yaml` | 3 | 75 | `047b2bcf53daa6d30ed5eb31d388d97e38b9c7bdd6d80728960cdb49218a419b` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/tidal/tidal/tidal.yaml) |
| loon | `loon/tidal/tidal/tidal.list` | 3 | 80 | `07a4be8f14c82aa2e6e5ba3f5513f18888e75e0d9ce8189ad1a30a091d936978` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/tidal/tidal/tidal.list) |
| mihomo | `mihomo/tidal/tidal/tidal.yaml` | 3 | 101 | `4431c12470db4be8e74408cff6138e7ac509a5d823a7b14129a8a8d7ae2ab843` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/tidal/tidal/tidal.yaml) |
| quantumultx | `quantumultx/tidal/tidal/tidal.list` | 3 | 98 | `fff62f3b098176b3686fc57ad0fdb1001f68e748a5c1673e53e31803db9907b4` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/tidal/tidal/tidal.list) |
| shadowrocket | `shadowrocket/tidal/tidal/tidal.list` | 3 | 80 | `07a4be8f14c82aa2e6e5ba3f5513f18888e75e0d9ce8189ad1a30a091d936978` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/tidal/tidal/tidal.list) |
| singbox | `singbox/tidal/tidal/tidal.json` | 0 | 152 | `c8f98531e31e5f0126169acece0076e741354e2e4431093697b37111964149ea` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/tidal/tidal/tidal.json) |
| surge | `surge/tidal/tidal/tidal.list` | 3 | 80 | `07a4be8f14c82aa2e6e5ba3f5513f18888e75e0d9ce8189ad1a30a091d936978` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/tidal/tidal/tidal.list) |

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