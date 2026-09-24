<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/lucide/service.svg" alt="Bahamut 图标" width="72" height="72">

# Bahamut — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `bahamut` |
| 类型 | service |
| Provider | `bahamut` |
| 语义规则数量 | **7** |
| 语义 SHA-256 | `87c3a0dc32c8c700be43c78458b1290bff33d6dfcb4939f001373ba216084922` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**lucide semantic fallback**

- Style：`lucide`
- Identity：`semantic.fallback.lucide`
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/lucide/service.svg`
- 该图标用于覆盖缺失身份，不代表官方品牌 Logo。

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/bahamut/bahamut/bahamut.yaml` | 7 | 167 | `41d0bc4db83afc92ba41e2ad85cc111491e6d7f1dfa4d8c93183997cc4b947d4` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/bahamut/bahamut/bahamut.yaml) |
| loon | `loon/bahamut/bahamut/bahamut.list` | 7 | 185 | `7db2e4f1a024b98375e6b9feab69cf9bea7ba81a2fbd33b9f9e3319759f97c44` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/bahamut/bahamut/bahamut.list) |
| mihomo | `mihomo/bahamut/bahamut/bahamut.yaml` | 7 | 222 | `c484754fa4f64fb5304feb739d44059ff16b945d860be32f164839a8e08a085c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/bahamut/bahamut/bahamut.yaml) |
| quantumultx | `quantumultx/bahamut/bahamut/bahamut.list` | 7 | 227 | `3d96c6585c75e312034d960133f5e81abb43ec6389e003e711527bc9f860c7a7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/bahamut/bahamut/bahamut.list) |
| shadowrocket | `shadowrocket/bahamut/bahamut/bahamut.list` | 7 | 185 | `7db2e4f1a024b98375e6b9feab69cf9bea7ba81a2fbd33b9f9e3319759f97c44` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/bahamut/bahamut/bahamut.list) |
| singbox | `singbox/bahamut/bahamut/bahamut.json` | 0 | 278 | `334c7a1df8c45e50b539f1ccd448ae0dc2927f0fdcb6fc2d2a0105fb4ef3f052` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/bahamut/bahamut/bahamut.json) |
| surge | `surge/bahamut/bahamut/bahamut.list` | 7 | 185 | `7db2e4f1a024b98375e6b9feab69cf9bea7ba81a2fbd33b9f9e3319759f97c44` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/bahamut/bahamut/bahamut.list) |

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