<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/tabler/service.svg" alt="Kuwo 图标" width="72" height="72">

# Kuwo — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `kuwo` |
| 类型 | service |
| Provider | `kuwo` |
| 语义规则数量 | **3** |
| 语义 SHA-256 | `56a09be2a42d3fd790d07df8d0a796499e6415f43d1c0d15a7f2dbc822a2c39b` |
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
| egern | `egern/kuwo/kuwo/kuwo.yaml` | 3 | 64 | `084dff057272b7b7978b7b5f33868746d7b37c1205b52f841feb65fb8a0c1d36` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/kuwo/kuwo/kuwo.yaml) |
| loon | `loon/kuwo/kuwo/kuwo.list` | 3 | 69 | `b9e07a995b53848adcc1c780e51e5ec4245da8824ffcc9e423496d07d6b9a4f6` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/kuwo/kuwo/kuwo.list) |
| mihomo | `mihomo/kuwo/kuwo/kuwo.yaml` | 3 | 90 | `b7abf22a0a31e483de018078ffd61e84c34af2fe6ee2006ada34e799506c1ec8` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/kuwo/kuwo/kuwo.yaml) |
| quantumultx | `quantumultx/kuwo/kuwo/kuwo.list` | 3 | 87 | `7f41146105332b46d6028255a37caf0d3e817d892c6245633c3a36c284421564` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/kuwo/kuwo/kuwo.list) |
| shadowrocket | `shadowrocket/kuwo/kuwo/kuwo.list` | 3 | 69 | `b9e07a995b53848adcc1c780e51e5ec4245da8824ffcc9e423496d07d6b9a4f6` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/kuwo/kuwo/kuwo.list) |
| singbox | `singbox/kuwo/kuwo/kuwo.json` | 0 | 141 | `89ce757c160348f9414bddf6fc4029cbc2372efeae722c4ac876168966e1a797` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/kuwo/kuwo/kuwo.json) |
| surge | `surge/kuwo/kuwo/kuwo.list` | 3 | 69 | `b9e07a995b53848adcc1c780e51e5ec4245da8824ffcc9e423496d07d6b9a4f6` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/kuwo/kuwo/kuwo.list) |

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