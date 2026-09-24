<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/remix/service.svg" alt="Kuaishou 图标" width="72" height="72">

# Kuaishou — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `kuaishou` |
| 类型 | service |
| Provider | `kuaishou` |
| 语义规则数量 | **678** |
| 语义 SHA-256 | `bad70f170bd920997f34bf6ac19e839f2c6a59c3d6ae0142b3c0aed5e4dad68e` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**remix semantic fallback**

- Style：`remix`
- Identity：`semantic.fallback.remix`
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/remix/service.svg`
- 该图标用于覆盖缺失身份，不代表官方品牌 Logo。

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/kuaishou/kuaishou/kuaishou.yaml` | 678 | 13798 | `e50f8f6410801fc368f6a022b3a672fa7a2bb2d1efba3b6a8f3aa31d1fbcd652` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/kuaishou/kuaishou/kuaishou.yaml) |
| loon | `loon/kuaishou/kuaishou/kuaishou.list` | 678 | 19203 | `7d3329c351f2809a71502d5c1cfac48a792c1283d3a9cd9f2309d372b54c8420` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/kuaishou/kuaishou/kuaishou.list) |
| mihomo | `mihomo/kuaishou/kuaishou/kuaishou.yaml` | 678 | 21924 | `9246af48bed0bf4f8c88e9cbfcda4d25c60f4c17ed3ffb89716ff80472dfcf0b` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/kuaishou/kuaishou/kuaishou.yaml) |
| quantumultx | `quantumultx/kuaishou/kuaishou/kuaishou.list` | 678 | 23271 | `5f9e3d6729f2d2ac718243de0c5f5a7789d5330368fe2b99e79ed36d35e10b48` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/kuaishou/kuaishou/kuaishou.list) |
| shadowrocket | `shadowrocket/kuaishou/kuaishou/kuaishou.list` | 678 | 19203 | `7d3329c351f2809a71502d5c1cfac48a792c1283d3a9cd9f2309d372b54c8420` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/kuaishou/kuaishou/kuaishou.list) |
| singbox | `singbox/kuaishou/kuaishou/kuaishou.json` | 0 | 17250 | `ff86f738d93a044cc83d6e5f70ba49264d27b2db13a5f3968e51c4b154c33ce7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/kuaishou/kuaishou/kuaishou.json) |
| surge | `surge/kuaishou/kuaishou/kuaishou.list` | 678 | 19203 | `7d3329c351f2809a71502d5c1cfac48a792c1283d3a9cd9f2309d372b54c8420` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/kuaishou/kuaishou/kuaishou.list) |

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