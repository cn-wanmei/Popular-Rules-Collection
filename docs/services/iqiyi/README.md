<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/bootstrap/service.svg" alt="iQIYI 图标" width="72" height="72">

# iQIYI — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `iqiyi_aggregate` |
| 类型 | provider_aggregate |
| Provider | `iqiyi` |
| 语义规则数量 | **67** |
| 语义 SHA-256 | `78f65e2cfd7982ae0a8ee36a32e5bed9028823fd9c5201d72a6bae6ac5540189` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**bootstrap semantic fallback**

- Style：`bootstrap`
- Identity：`semantic.fallback.bootstrap`
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/bootstrap/service.svg`
- 该图标用于覆盖缺失身份，不代表官方品牌 Logo。

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/iqiyi/iqiyi.yaml` | 66 | 1369 | `f0485ee645e6748bb9ba5bb9fc1c5465ddeff301f27d457e77a8d9f11eb65b85` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/iqiyi/iqiyi.yaml) |
| loon | `loon/iqiyi/iqiyi.list` | 66 | 1720 | `379b5589a055a800eff0c59eb732a42cd2f7597b2ad2c024d4e79389348b201a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/iqiyi/iqiyi.list) |
| mihomo | `mihomo/iqiyi/iqiyi.yaml` | 66 | 1993 | `5c171d602c394f57d576d768ef8f37c36c7cd4de8e9aab555a9d6d879578c1b9` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/iqiyi/iqiyi.yaml) |
| quantumultx | `quantumultx/iqiyi/iqiyi.list` | 66 | 2158 | `ae4f3113d7b682085aa9a1fd0892013ed6707c3ea2ce6d4f8d6206b78329137a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/iqiyi/iqiyi.list) |
| shadowrocket | `shadowrocket/iqiyi/iqiyi.list` | 66 | 1720 | `379b5589a055a800eff0c59eb732a42cd2f7597b2ad2c024d4e79389348b201a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/iqiyi/iqiyi.list) |
| singbox | `singbox/iqiyi/iqiyi.json` | 0 | 1789 | `82f640b766dca94c1d401e67f33c3b71775b675a1209fc2bd6dc95efb044293e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/iqiyi/iqiyi.json) |
| surge | `surge/iqiyi/iqiyi.list` | 66 | 1720 | `379b5589a055a800eff0c59eb732a42cd2f7597b2ad2c024d4e79389348b201a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/iqiyi/iqiyi.list) |

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