<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/fluent/service.svg" alt="ByteDance 图标" width="72" height="72">

# ByteDance — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `bytedance` |
| 类型 | provider_aggregate |
| Provider | `bytedance` |
| 语义规则数量 | **1082** |
| 语义 SHA-256 | `04fab94e04296c75ea6864e5531af5a15a6c8da7fe015b21482cfe522f9af6ae` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**fluent semantic fallback**

- Style：`fluent`
- Identity：`semantic.fallback.fluent`
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/fluent/service.svg`
- 该图标用于覆盖缺失身份，不代表官方品牌 Logo。

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/bytedance/bytedance.yaml` | 1081 | 22845 | `ee09c1ad061e6cb1e8bae6f92e3d27c59e99af64abb561ea24645e011a5ba367` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/bytedance/bytedance.yaml) |
| loon | `loon/bytedance/bytedance.list` | 1081 | 31436 | `20465ed9d7b1961cfd1869bbabf1d9d143a2a9a6202bd29d302396a87fc48135` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/bytedance/bytedance.list) |
| mihomo | `mihomo/bytedance/bytedance.yaml` | 1081 | 35769 | `336a1f03b254782b9ced6532e189b55e76b1edb23fed9f72466791e25a513a52` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/bytedance/bytedance.yaml) |
| quantumultx | `quantumultx/bytedance/bytedance.list` | 1081 | 37924 | `2c2cfab4488a4b46dd223a145d8a3d9f6db0d75903f20a83035e798761a64265` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/bytedance/bytedance.list) |
| shadowrocket | `shadowrocket/bytedance/bytedance.list` | 1081 | 31436 | `20465ed9d7b1961cfd1869bbabf1d9d143a2a9a6202bd29d302396a87fc48135` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/bytedance/bytedance.list) |
| singbox | `singbox/bytedance/bytedance.json` | 0 | 28340 | `539d988198ecf12787f03f5383b5b5f73463e3904383e2563e7af1cab759241f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/bytedance/bytedance.json) |
| surge | `surge/bytedance/bytedance.list` | 1081 | 31436 | `20465ed9d7b1961cfd1869bbabf1d9d143a2a9a6202bd29d302396a87fc48135` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/bytedance/bytedance.list) |

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