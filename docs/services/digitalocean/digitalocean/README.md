<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/digitalocean.png" alt="DigitalOcean 图标" width="72" height="72">

# DigitalOcean — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `digitalocean` |
| 类型 | service |
| Provider | `digitalocean` |
| 语义规则数量 | **6** |
| 语义 SHA-256 | `9090521e3ea4c8376f98a2f083325a28c021286d67949ac14b7efaa0533e2822` |
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
| egern | `egern/digitalocean/digitalocean/digitalocean.yaml` | 10 | 240 | `37a0f4163cfc7e8ab15b80ed0ad6af273e5205bcd7f4bfc718cbe4e02f700ee7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/digitalocean/digitalocean/digitalocean.yaml) |
| loon | `loon/digitalocean/digitalocean/digitalocean.list` | 10 | 301 | `389a06f23960738b67b5869ceda22b77e2e0f0d2e74bcdd019e14a78497525b9` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/digitalocean/digitalocean/digitalocean.list) |
| mihomo | `mihomo/digitalocean/digitalocean/digitalocean.yaml` | 10 | 350 | `a168b98717b52c09ac97f75b167e0da45c26e2db9b3e890d45057a2162a9439b` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/digitalocean/digitalocean/digitalocean.yaml) |
| quantumultx | `quantumultx/digitalocean/digitalocean/digitalocean.list` | 10 | 361 | `acc2a6862e6738933ed8d01795b1ac03a2b3bfd62d9e274036b51d1303f32045` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/digitalocean/digitalocean/digitalocean.list) |
| shadowrocket | `shadowrocket/digitalocean/digitalocean/digitalocean.list` | 10 | 301 | `389a06f23960738b67b5869ceda22b77e2e0f0d2e74bcdd019e14a78497525b9` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/digitalocean/digitalocean/digitalocean.list) |
| singbox | `singbox/digitalocean/digitalocean/digitalocean.json` | 0 | 352 | `1ca5261979b0711e6a30a64d66c0747be40fd43d53af001d12963487b6c35d85` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/digitalocean/digitalocean/digitalocean.json) |
| surge | `surge/digitalocean/digitalocean/digitalocean.list` | 10 | 301 | `389a06f23960738b67b5869ceda22b77e2e0f0d2e74bcdd019e14a78497525b9` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/digitalocean/digitalocean/digitalocean.list) |

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