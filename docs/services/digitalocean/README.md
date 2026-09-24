<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/digitalocean.png" alt="DigitalOcean 图标" width="72" height="72">

# DigitalOcean — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `digitalocean_aggregate` |
| 类型 | provider_aggregate |
| Provider | `digitalocean` |
| 语义规则数量 | **6** |
| 语义 SHA-256 | `3fa543cc02689032fbfc90e478bb5398454d618dd8965f90fd1a12f0f0414fea` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.digitalocean`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/digitalocean.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/digitalocean/digitalocean.yaml` | 6 | 155 | `9954c4b21970cdb434a0e50ec8fd621419c6b2176d086d77add359f215251ffe` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/digitalocean/digitalocean.yaml) |
| loon | `loon/digitalocean/digitalocean.list` | 6 | 184 | `2249f4d9d7c087a734121fecc705b64d2436f16c60c51b9f4749b2660d3f58d2` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/digitalocean/digitalocean.list) |
| mihomo | `mihomo/digitalocean/digitalocean.yaml` | 6 | 217 | `e0765730bbe25bc1b34f7ae593d3d0929415411cecd63d3b2c9982956a45e0d3` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/digitalocean/digitalocean.yaml) |
| quantumultx | `quantumultx/digitalocean/digitalocean.list` | 6 | 220 | `f9e5ff9003edf3d47bf33b74e25049a4e3784f11d84a257db81c398f51f84e5b` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/digitalocean/digitalocean.list) |
| shadowrocket | `shadowrocket/digitalocean/digitalocean.list` | 6 | 184 | `2249f4d9d7c087a734121fecc705b64d2436f16c60c51b9f4749b2660d3f58d2` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/digitalocean/digitalocean.list) |
| singbox | `singbox/digitalocean/digitalocean.json` | 0 | 247 | `839a5dc050a31cf15618026c1f5d80dd186c978bf81b284fb2318f502449d2d3` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/digitalocean/digitalocean.json) |
| surge | `surge/digitalocean/digitalocean.list` | 6 | 184 | `2249f4d9d7c087a734121fecc705b64d2436f16c60c51b9f4749b2660d3f58d2` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/digitalocean/digitalocean.list) |

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