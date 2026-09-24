<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/solar/service.svg" alt="Riot Games 图标" width="72" height="72">

# Riot Games — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `riotgames` |
| 类型 | service |
| Provider | `riotgames` |
| 语义规则数量 | **55** |
| 语义 SHA-256 | `3c18ba9857086eff4dd21698a30f580e16928d1c87f35c4938541a1a2507f4c2` |
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
| egern | `egern/riotgames/riotgames/riotgames.yaml` | 55 | 1228 | `2fa978d3e0cff328e278bdfa190592f269ca74b529bc5ea74de1114e135134a5` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/riotgames/riotgames/riotgames.yaml) |
| loon | `loon/riotgames/riotgames/riotgames.list` | 55 | 1649 | `c0f5595e705d1d00f039c38e2a2782735d77fb6084287f0f431339fc1d1b82e3` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/riotgames/riotgames/riotgames.list) |
| mihomo | `mihomo/riotgames/riotgames/riotgames.yaml` | 55 | 1878 | `0533cd3eb11d5b73cf5c7acd12e0d9462b42a2b593a9a7144bdc114ee4691f90` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/riotgames/riotgames/riotgames.yaml) |
| quantumultx | `quantumultx/riotgames/riotgames/riotgames.list` | 55 | 1979 | `7bf917d61f87304ccd7bfcd5c559c097fba6b32583e67fc74c6fd942d7d5425f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/riotgames/riotgames/riotgames.list) |
| shadowrocket | `shadowrocket/riotgames/riotgames/riotgames.list` | 55 | 1649 | `c0f5595e705d1d00f039c38e2a2782735d77fb6084287f0f431339fc1d1b82e3` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/riotgames/riotgames/riotgames.list) |
| singbox | `singbox/riotgames/riotgames/riotgames.json` | 0 | 1565 | `1386c0c863ca1899bc58e3d05851e171dcc0ba929ffdae061a1a3b0e4dbf4b08` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/riotgames/riotgames/riotgames.json) |
| surge | `surge/riotgames/riotgames/riotgames.list` | 55 | 1649 | `c0f5595e705d1d00f039c38e2a2782735d77fb6084287f0f431339fc1d1b82e3` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/riotgames/riotgames/riotgames.list) |

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