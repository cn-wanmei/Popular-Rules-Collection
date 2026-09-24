<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/whatsapp.png" alt="WhatsApp 图标" width="72" height="72">

# WhatsApp — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `whatsapp` |
| 类型 | service |
| Provider | `meta` |
| 语义规则数量 | **28** |
| 语义 SHA-256 | `fd5d63f8e4f2af432984f92995149a6dcea48755d988ef454df1d08c17b3d043` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.whatsapp`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/whatsapp.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/meta/whatsapp/whatsapp.yaml` | 43 | 969 | `440be5f308d3d9bb890b7453e5f75cb2f7e5125bf16ca50834ce648fdca8f529` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/meta/whatsapp/whatsapp.yaml) |
| loon | `loon/meta/whatsapp/whatsapp.list` | 43 | 1177 | `a216d81d3c88b48532c0583d1a49afbe081ed566ad8528941610df56d03c4cf1` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/meta/whatsapp/whatsapp.list) |
| mihomo | `mihomo/meta/whatsapp/whatsapp.yaml` | 43 | 1358 | `576da564a63595365710547673ed9a1c7a42aa4085842c93255e01b43a669cdf` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/meta/whatsapp/whatsapp.yaml) |
| quantumultx | `quantumultx/meta/whatsapp/whatsapp.list` | 43 | 1457 | `1960d08eb6942fb1535da6ec0cd97e345003fe699a9990060e822f38a67cd85d` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/meta/whatsapp/whatsapp.list) |
| shadowrocket | `shadowrocket/meta/whatsapp/whatsapp.list` | 43 | 1177 | `a216d81d3c88b48532c0583d1a49afbe081ed566ad8528941610df56d03c4cf1` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/meta/whatsapp/whatsapp.list) |
| singbox | `singbox/meta/whatsapp/whatsapp.json` | 0 | 1288 | `a4360dcc4b908972b71da87e4605fe2cfd106d19735921e2cdd0e6c25a0fb564` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/meta/whatsapp/whatsapp.json) |
| surge | `surge/meta/whatsapp/whatsapp.list` | 43 | 1177 | `a216d81d3c88b48532c0583d1a49afbe081ed566ad8528941610df56d03c4cf1` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/meta/whatsapp/whatsapp.list) |

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