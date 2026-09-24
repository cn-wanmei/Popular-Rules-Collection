<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/heroicons/service.svg" alt="Dewu 图标" width="72" height="72">

# Dewu — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `dewu` |
| 类型 | service |
| Provider | `dewu` |
| 语义规则数量 | **45** |
| 语义 SHA-256 | `b1f5364fd101eef1c96080c9a0581e1327148bdf17fc55ca9d9577150a6061b3` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**heroicons semantic fallback**

- Style：`heroicons`
- Identity：`semantic.fallback.heroicons`
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/heroicons/service.svg`
- 该图标用于覆盖缺失身份，不代表官方品牌 Logo。

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/dewu/dewu/dewu.yaml` | 45 | 889 | `49d6d41673f9594c5941617fa7d386c3fcfd8f87a8909e903560c5db1cb13f25` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/dewu/dewu/dewu.yaml) |
| loon | `loon/dewu/dewu/dewu.list` | 45 | 1230 | `0238f43dc255f1f173fcfd9cf756e89dac238dd1c4de45dfbeb85c5e8ad4440a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/dewu/dewu/dewu.list) |
| mihomo | `mihomo/dewu/dewu/dewu.yaml` | 45 | 1419 | `36caf47fcc5a6aba53eab1d1c6cb7bdcb31200d0827eae3eec7c49e0c46bde5e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/dewu/dewu/dewu.yaml) |
| quantumultx | `quantumultx/dewu/dewu/dewu.list` | 45 | 1500 | `ebe20e849baf7a9cc61b1d78192890ad6274f39296fe16bd94c6d517a7c6e4c0` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/dewu/dewu/dewu.list) |
| shadowrocket | `shadowrocket/dewu/dewu/dewu.list` | 45 | 1230 | `0238f43dc255f1f173fcfd9cf756e89dac238dd1c4de45dfbeb85c5e8ad4440a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/dewu/dewu/dewu.list) |
| singbox | `singbox/dewu/dewu/dewu.json` | 0 | 1176 | `9f40b7013dc63260e761fe4ae908d61bdb0cab87ac0b7b487a2e276817a01834` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/dewu/dewu/dewu.json) |
| surge | `surge/dewu/dewu/dewu.list` | 45 | 1230 | `0238f43dc255f1f173fcfd9cf756e89dac238dd1c4de45dfbeb85c5e8ad4440a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/dewu/dewu/dewu.list) |

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