<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/heroicons/service.svg" alt="Minecraft 图标" width="72" height="72">

# Minecraft — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `minecraft` |
| 类型 | service |
| Provider | `microsoft` |
| 语义规则数量 | **6** |
| 语义 SHA-256 | `fab8f97007b16a6a14c8cbec9602c9488f40c0fdb2cf05cc200d59d963261a19` |
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
| egern | `egern/microsoft/minecraft/minecraft.yaml` | 12 | 299 | `dd69b6e4ec48d554e3aa059aa0d4d11b9538c8872691bbb7030f0893c551ef41` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/microsoft/minecraft/minecraft.yaml) |
| loon | `loon/microsoft/minecraft/minecraft.list` | 12 | 376 | `44ec9110ffab12195445cefe93b3ac874bdb4e60e602baeaca15eee48d3a0380` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/microsoft/minecraft/minecraft.list) |
| mihomo | `mihomo/microsoft/minecraft/minecraft.yaml` | 12 | 433 | `0baa5e0dcbd9c787dbac3b9e7a702054183a706fd9925f8537668e1eef353a4b` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/microsoft/minecraft/minecraft.yaml) |
| quantumultx | `quantumultx/microsoft/minecraft/minecraft.list` | 12 | 448 | `e010df5d0f7df454baea1824141cc1895e7bd037ff55b37f8a3b5dbc779dda45` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/microsoft/minecraft/minecraft.list) |
| shadowrocket | `shadowrocket/microsoft/minecraft/minecraft.list` | 12 | 376 | `44ec9110ffab12195445cefe93b3ac874bdb4e60e602baeaca15eee48d3a0380` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/microsoft/minecraft/minecraft.list) |
| singbox | `singbox/microsoft/minecraft/minecraft.json` | 0 | 421 | `edaaf87f1bc70bd02d4980665cce7d17de450b46ca27bd90e1e0536d0b77e93a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/microsoft/minecraft/minecraft.json) |
| surge | `surge/microsoft/minecraft/minecraft.list` | 12 | 376 | `44ec9110ffab12195445cefe93b3ac874bdb4e60e602baeaca15eee48d3a0380` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/microsoft/minecraft/minecraft.list) |

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