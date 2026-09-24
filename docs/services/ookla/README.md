<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/tabler/service.svg" alt="Ookla 图标" width="72" height="72">

# Ookla — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `ookla_aggregate` |
| 类型 | provider_aggregate |
| Provider | `ookla` |
| 语义规则数量 | **5** |
| 语义 SHA-256 | `5bce5b79155af07e305886fd50c5bedd5f9ae2b6ebc2dcfc4465a301f9f4d04d` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**tabler semantic fallback**

- Style：`tabler`
- Identity：`semantic.fallback.tabler`
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/tabler/service.svg`
- 该图标用于覆盖缺失身份，不代表官方品牌 Logo。

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/ookla/ookla.yaml` | 5 | 139 | `fddf6a0cd0405eb0df64b7a1481f09d015b3726bdb8dd07a28f5bcef1538a506` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/ookla/ookla.yaml) |
| loon | `loon/ookla/ookla.list` | 5 | 141 | `2afddc6308519953c25950623b85e444f4f7321ca5e4d1935c3006575c288500` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/ookla/ookla.list) |
| mihomo | `mihomo/ookla/ookla.yaml` | 5 | 170 | `6c0f4c0c66c8357e334f8d47c57c2139b6fc682960dd71e269b7f058856e53b1` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/ookla/ookla.yaml) |
| quantumultx | `quantumultx/ookla/ookla.list` | 5 | 171 | `26f2743280ed4df9280a86ab695b945e0b4a892a98d030d8b56341b14c2b6a61` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/ookla/ookla.list) |
| shadowrocket | `shadowrocket/ookla/ookla.list` | 5 | 141 | `2afddc6308519953c25950623b85e444f4f7321ca5e4d1935c3006575c288500` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/ookla/ookla.list) |
| singbox | `singbox/ookla/ookla.json` | 0 | 240 | `a0ce8c3e3377e28f3ea77585a7e495dab4e4f186a2774560c4b9c03850a29380` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/ookla/ookla.json) |
| surge | `surge/ookla/ookla.list` | 5 | 141 | `2afddc6308519953c25950623b85e444f4f7321ca5e4d1935c3006575c288500` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/ookla/ookla.list) |

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