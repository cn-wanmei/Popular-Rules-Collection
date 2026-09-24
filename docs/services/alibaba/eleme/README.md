<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/tabler/service.svg" alt="Ele.me 图标" width="72" height="72">

# Ele.me — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `eleme` |
| 类型 | service |
| Provider | `alibaba` |
| 语义规则数量 | **13** |
| 语义 SHA-256 | `df0e6e9cfd914f85c76f94fd7c23ff2fe009482bb1eef06023f32b2de6d0cd27` |
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
| egern | `egern/alibaba/eleme/eleme.yaml` | 13 | 259 | `2a568a652fd884ac97f4203caad0a8f509ca13b254f3e47667a5495bf62fde75` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/alibaba/eleme/eleme.yaml) |
| loon | `loon/alibaba/eleme/eleme.list` | 13 | 344 | `e2e25b8f85866b1cf86c6c4b960cc683f68dffe6cb909846a4c6ab18882ba732` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/alibaba/eleme/eleme.list) |
| mihomo | `mihomo/alibaba/eleme/eleme.yaml` | 13 | 405 | `6364ca9cc6acdb40a947674437e32ea16dbd2f257b851d4f8f2cdb749b9f1483` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/alibaba/eleme/eleme.yaml) |
| quantumultx | `quantumultx/alibaba/eleme/eleme.list` | 13 | 422 | `e75063a445d4888f2596d08aa3c4575882f18c4610fd8a624e1464e4af36de4a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/alibaba/eleme/eleme.list) |
| shadowrocket | `shadowrocket/alibaba/eleme/eleme.list` | 13 | 344 | `e2e25b8f85866b1cf86c6c4b960cc683f68dffe6cb909846a4c6ab18882ba732` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/alibaba/eleme/eleme.list) |
| singbox | `singbox/alibaba/eleme/eleme.json` | 0 | 386 | `d4374262eb9bad52c8de1f202f458ac9c388b82ddeff015c52c371316ffcc52b` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/alibaba/eleme/eleme.json) |
| surge | `surge/alibaba/eleme/eleme.list` | 13 | 344 | `e2e25b8f85866b1cf86c6c4b960cc683f68dffe6cb909846a4c6ab18882ba732` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/alibaba/eleme/eleme.list) |

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