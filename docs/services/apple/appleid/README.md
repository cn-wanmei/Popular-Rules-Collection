<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/lucide/service.svg" alt="Apple ID 图标" width="72" height="72">

# Apple ID — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `appleid` |
| 类型 | service |
| Provider | `apple` |
| 语义规则数量 | **4** |
| 语义 SHA-256 | `1d1aac6f32327d231c21abb218c8b3cad184c320e24cd9f67fe401ae37817f5c` |
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
| egern | `egern/apple/appleid/appleid.yaml` | 4 | 106 | `5fd0f463893648d0adbff0870a8b43a6cb30ef837e6a15464252816b9e1e48e3` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/apple/appleid/appleid.yaml) |
| loon | `loon/apple/appleid/appleid.list` | 4 | 98 | `3ca0886fa6dda3a88aa98226a467737859e40dd3d109cd447d4ebab39d7454e3` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/apple/appleid/appleid.list) |
| mihomo | `mihomo/apple/appleid/appleid.yaml` | 4 | 123 | `e72f0c77c4e00a5afbd76c9da613b55f8c19eef63ba33f7b2533a33beca088ea` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/apple/appleid/appleid.yaml) |
| quantumultx | `quantumultx/apple/appleid/appleid.list` | 4 | 122 | `9bfc37a2cf03b997c3c9bf33c70f3635cc6824382ebb3f8f308e8d53e5634f62` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/apple/appleid/appleid.list) |
| shadowrocket | `shadowrocket/apple/appleid/appleid.list` | 4 | 98 | `3ca0886fa6dda3a88aa98226a467737859e40dd3d109cd447d4ebab39d7454e3` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/apple/appleid/appleid.list) |
| singbox | `singbox/apple/appleid/appleid.json` | 0 | 188 | `c901f72dde71c37b7cb1597a520b4a17fb31806bcc92656b35657f942b893d83` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/apple/appleid/appleid.json) |
| surge | `surge/apple/appleid/appleid.list` | 4 | 98 | `3ca0886fa6dda3a88aa98226a467737859e40dd3d109cd447d4ebab39d7454e3` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/apple/appleid/appleid.list) |

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