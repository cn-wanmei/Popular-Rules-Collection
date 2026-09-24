<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/chinatelecom.png" alt="China Telecom 图标" width="72" height="72">

# China Telecom — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `chinatelecom` |
| 类型 | service |
| Provider | `chinatelecom` |
| 语义规则数量 | **83** |
| 语义 SHA-256 | `66238671fc323266b70e40599c7fd7090dc436ba02b331b712c80d288b453496` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`semantic.chinatelecom`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/chinatelecom.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/chinatelecom/chinatelecom/chinatelecom.yaml` | 83 | 1527 | `bd118848a15807d33e3e3e379954bf9bfb3591c18ecf5983a25b50facfe9a175` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/chinatelecom/chinatelecom/chinatelecom.yaml) |
| loon | `loon/chinatelecom/chinatelecom/chinatelecom.list` | 83 | 2172 | `0a3547dd20fc6838491ca93fa19e4bcbe69aa52450b61ed162334c387ef7ff0a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/chinatelecom/chinatelecom/chinatelecom.list) |
| mihomo | `mihomo/chinatelecom/chinatelecom/chinatelecom.yaml` | 83 | 2513 | `27ee4f67cae083456d940e10f12ba21cd68bf3247fccafaabb9d0bedf5893114` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/chinatelecom/chinatelecom/chinatelecom.yaml) |
| quantumultx | `quantumultx/chinatelecom/chinatelecom/chinatelecom.list` | 83 | 2670 | `53ac2c7382c47a71e2d2a87d40574812e41be79a009e12d567ea7403c3a780a5` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/chinatelecom/chinatelecom/chinatelecom.list) |
| shadowrocket | `shadowrocket/chinatelecom/chinatelecom/chinatelecom.list` | 83 | 2172 | `0a3547dd20fc6838491ca93fa19e4bcbe69aa52450b61ed162334c387ef7ff0a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/chinatelecom/chinatelecom/chinatelecom.list) |
| singbox | `singbox/chinatelecom/chinatelecom/chinatelecom.json` | 0 | 2004 | `640f93a883cba262ecbd444cafd715db7e57c7e282732ec38193ac71ff47655b` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/chinatelecom/chinatelecom/chinatelecom.json) |
| surge | `surge/chinatelecom/chinatelecom/chinatelecom.list` | 83 | 2172 | `0a3547dd20fc6838491ca93fa19e4bcbe69aa52450b61ed162334c387ef7ff0a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/chinatelecom/chinatelecom/chinatelecom.list) |

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