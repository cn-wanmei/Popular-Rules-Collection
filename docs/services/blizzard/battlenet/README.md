<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/lucide/service.svg" alt="Battle.net 图标" width="72" height="72">

# Battle.net — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `battlenet` |
| 类型 | service |
| Provider | `blizzard` |
| 语义规则数量 | **62** |
| 语义 SHA-256 | `7a68f906db296f21696efcf6737973c702012f0510dcbe12368e3301e00b1aae` |
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
| egern | `egern/blizzard/battlenet/battlenet.yaml` | 62 | 1552 | `f271d0b7de9fd6b775a7de07b9d12516a18dc484c225d990d308212b09441d6f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/blizzard/battlenet/battlenet.yaml) |
| loon | `loon/blizzard/battlenet/battlenet.list` | 62 | 1878 | `92375aa2e7eeb6fc69ff0d77ed54d0358116918e94bb284b770ecc0fd1a470cd` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/blizzard/battlenet/battlenet.list) |
| mihomo | `mihomo/blizzard/battlenet/battlenet.yaml` | 62 | 2135 | `acaf8eb5c5ed140abefe0293476c6b20ee698994816dda57641b98c1f8f880a5` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/blizzard/battlenet/battlenet.yaml) |
| quantumultx | `quantumultx/blizzard/battlenet/battlenet.list` | 62 | 2296 | `c8f76cc9bd408d2e172679bd44e18463332eb831beec3b8edf43128316c66a85` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/blizzard/battlenet/battlenet.list) |
| shadowrocket | `shadowrocket/blizzard/battlenet/battlenet.list` | 62 | 1878 | `92375aa2e7eeb6fc69ff0d77ed54d0358116918e94bb284b770ecc0fd1a470cd` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/blizzard/battlenet/battlenet.list) |
| singbox | `singbox/blizzard/battlenet/battlenet.json` | 0 | 1938 | `e311972e672207b233025c7f30aef242c676657b6c126b474984d04a443c693e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/blizzard/battlenet/battlenet.json) |
| surge | `surge/blizzard/battlenet/battlenet.list` | 62 | 1878 | `92375aa2e7eeb6fc69ff0d77ed54d0358116918e94bb284b770ecc0fd1a470cd` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/blizzard/battlenet/battlenet.list) |

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