<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/solar/service.svg" alt="China Construction Bank 图标" width="72" height="72">

# China Construction Bank — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `ccb` |
| 类型 | service |
| Provider | `ccb` |
| 语义规则数量 | **18** |
| 语义 SHA-256 | `923aab5c4383df1ab267f73e84980bc2ae57ab5599664c8e8428167a939bb060` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**solar semantic fallback**

- Style：`solar`
- Identity：`semantic.fallback.solar`
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/solar/service.svg`
- 该图标用于覆盖缺失身份，不代表官方品牌 Logo。

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/ccb/ccb/ccb.yaml` | 18 | 359 | `9716c8cdb21fa69dfd23690cceeb6a695a01a86b47cb93f75d00c5976cd7236f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/ccb/ccb/ccb.yaml) |
| loon | `loon/ccb/ccb/ccb.list` | 18 | 484 | `4fbb42d559766a02752a129fd1443be36b012c13627b297d26e280ee62534269` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/ccb/ccb/ccb.list) |
| mihomo | `mihomo/ccb/ccb/ccb.yaml` | 18 | 565 | `4a93f03ddf89ad70b0a9001f601cecdeb091828bd0914e0d089fdb11283ce0f9` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/ccb/ccb/ccb.yaml) |
| quantumultx | `quantumultx/ccb/ccb/ccb.list` | 18 | 592 | `bee812fb9048e9da006f3ff316b5d36ab284b99fcdc313a197817a2a1d174a53` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/ccb/ccb/ccb.list) |
| shadowrocket | `shadowrocket/ccb/ccb/ccb.list` | 18 | 484 | `4fbb42d559766a02752a129fd1443be36b012c13627b297d26e280ee62534269` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/ccb/ccb/ccb.list) |
| singbox | `singbox/ccb/ccb/ccb.json` | 0 | 511 | `f9ec45a58202fa0e4e38e566ea32ce4956cc814ce969ebfbda7ff51e38f09188` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/ccb/ccb/ccb.json) |
| surge | `surge/ccb/ccb/ccb.list` | 18 | 484 | `4fbb42d559766a02752a129fd1443be36b012c13627b297d26e280ee62534269` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/ccb/ccb/ccb.list) |

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