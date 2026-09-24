<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/weibo.png" alt="Weibo 图标" width="72" height="72">

# Weibo — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `weibo_aggregate` |
| 类型 | provider_aggregate |
| Provider | `weibo` |
| 语义规则数量 | **4** |
| 语义 SHA-256 | `a786a7b97e6dc7268d171b29278c69ddf92593cea7984a66acded87b6147ec6b` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.weibo`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/weibo.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/weibo/weibo.yaml` | 4 | 101 | `82cb4e089896384a1cb566a38f162742e063fb6eba1dea169a21bb57bc0d9525` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/weibo/weibo.yaml) |
| loon | `loon/weibo/weibo.list` | 4 | 95 | `cca288fcaa0bb197f7695b629f2f89c95ce2883d68bde6ff57bdbc0bcba1d91c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/weibo/weibo.list) |
| mihomo | `mihomo/weibo/weibo.yaml` | 4 | 120 | `11bd66f917f68fc08d485340e7620dfca42955955de4cb7820ac7a86d707950e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/weibo/weibo.yaml) |
| quantumultx | `quantumultx/weibo/weibo.list` | 4 | 119 | `3e36a07ec4f766c1eb16ab8cd3a2617a543d4ef2e82ec5d8134757cd4967fd6d` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/weibo/weibo.list) |
| shadowrocket | `shadowrocket/weibo/weibo.list` | 4 | 95 | `cca288fcaa0bb197f7695b629f2f89c95ce2883d68bde6ff57bdbc0bcba1d91c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/weibo/weibo.list) |
| singbox | `singbox/weibo/weibo.json` | 0 | 197 | `168941fedb7d0ec1f3a3dc4520285fbaf99358dda7464c529a3072038a705c76` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/weibo/weibo.json) |
| surge | `surge/weibo/weibo.list` | 4 | 95 | `cca288fcaa0bb197f7695b629f2f89c95ce2883d68bde6ff57bdbc0bcba1d91c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/weibo/weibo.list) |

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