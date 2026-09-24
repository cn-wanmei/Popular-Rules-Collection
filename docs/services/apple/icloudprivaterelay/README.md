<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/material-symbols/service.svg" alt="iCloud Private Relay 图标" width="72" height="72">

# iCloud Private Relay — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `icloudprivaterelay` |
| 类型 | service |
| Provider | `apple` |
| 语义规则数量 | **6** |
| 语义 SHA-256 | `8ee281cbb2245a9aa9c9b278514b6079dbfaf0cdcd37c435aaf22d1d2fc3e7f1` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**material-symbols semantic fallback**

- Style：`material-symbols`
- Identity：`semantic.fallback.material-symbols`
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/material-symbols/service.svg`
- 该图标用于覆盖缺失身份，不代表官方品牌 Logo。

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/apple/icloudprivaterelay/icloudprivaterelay.yaml` | 6 | 188 | `c32c92f5cb8632017d4831dcac68fe54cfb1565183c1726a82334fd82279985e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/apple/icloudprivaterelay/icloudprivaterelay.yaml) |
| loon | `loon/apple/icloudprivaterelay/icloudprivaterelay.list` | 6 | 177 | `bf918251648db75d5218ce67d009fbcf3de10dd6a74f596b67dfa869218bd494` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/apple/icloudprivaterelay/icloudprivaterelay.list) |
| mihomo | `mihomo/apple/icloudprivaterelay/icloudprivaterelay.yaml` | 6 | 210 | `0fdc63f3aeb89dc5f5626224b9c4c09cb8a7425824132c5b16fda8f133f46323` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/apple/icloudprivaterelay/icloudprivaterelay.yaml) |
| quantumultx | `quantumultx/apple/icloudprivaterelay/icloudprivaterelay.list` | 6 | 213 | `5a10d4d1c4e98ab0c720fd649f186f5a1a0defd32243198f2f9af720c96481d8` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/apple/icloudprivaterelay/icloudprivaterelay.list) |
| shadowrocket | `shadowrocket/apple/icloudprivaterelay/icloudprivaterelay.list` | 6 | 177 | `bf918251648db75d5218ce67d009fbcf3de10dd6a74f596b67dfa869218bd494` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/apple/icloudprivaterelay/icloudprivaterelay.list) |
| singbox | `singbox/apple/icloudprivaterelay/icloudprivaterelay.json` | 0 | 294 | `487181afc53a66cae440f0de4fe4816499164db300dd4127df2343ce9054e58c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/apple/icloudprivaterelay/icloudprivaterelay.json) |
| surge | `surge/apple/icloudprivaterelay/icloudprivaterelay.list` | 6 | 177 | `bf918251648db75d5218ce67d009fbcf3de10dd6a74f596b67dfa869218bd494` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/apple/icloudprivaterelay/icloudprivaterelay.list) |

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