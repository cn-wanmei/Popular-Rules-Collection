<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/hbo.png" alt="HBO 图标" width="72" height="72">

# HBO — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `hbo_aggregate` |
| 类型 | provider_aggregate |
| Provider | `hbo` |
| 语义规则数量 | **48** |
| 语义 SHA-256 | `689382148e81399d14833955237a8a941d7c74d06977f217f1a07b2fcf76ffaf` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.hbo`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/hbo.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/hbo/hbo.yaml` | 47 | 1170 | `5971600bbc802939c7b4bb5ac14b19ddbe4793ae7e2785d81ed311de05a046ec` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/hbo/hbo.yaml) |
| loon | `loon/hbo/hbo.list` | 47 | 1527 | `e10543a170bc2b6a3207be4d8a0ed8fd811228a09ccb368c0a894d1223045408` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/hbo/hbo.list) |
| mihomo | `mihomo/hbo/hbo.yaml` | 47 | 1724 | `9deb40b7757a4aeaf42c5f6a23743d6bf178f43a0e25af64385e3acb0f4b8f1c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/hbo/hbo.yaml) |
| quantumultx | `quantumultx/hbo/hbo.list` | 47 | 1809 | `cb5a8a056f7372e55cb0e8975b729b8163dd28be8d552be6281509993782552c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/hbo/hbo.list) |
| shadowrocket | `shadowrocket/hbo/hbo.list` | 47 | 1527 | `e10543a170bc2b6a3207be4d8a0ed8fd811228a09ccb368c0a894d1223045408` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/hbo/hbo.list) |
| singbox | `singbox/hbo/hbo.json` | 0 | 1467 | `1cf787cc765343a6ee626e3f17c716b1f679cb039815ff2ad9783b748bddd87e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/hbo/hbo.json) |
| surge | `surge/hbo/hbo.list` | 47 | 1527 | `e10543a170bc2b6a3207be4d8a0ed8fd811228a09ccb368c0a894d1223045408` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/hbo/hbo.list) |

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