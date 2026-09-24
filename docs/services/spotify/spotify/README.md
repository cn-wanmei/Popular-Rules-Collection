<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/spotify.png" alt="Spotify 图标" width="72" height="72">

# Spotify — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `spotify` |
| 类型 | service |
| Provider | `spotify` |
| 语义规则数量 | **38** |
| 语义 SHA-256 | `0eee92f7e3b61de22168a5bd03bc4eabb653b965adaf01ef2bdd8063ac765b0d` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.spotify`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/spotify.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/spotify/spotify/spotify.yaml` | 62 | 1657 | `1617ff56edd32bc606023780c4a02e755b417abad3c60d91a03278ecce239db4` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/spotify/spotify/spotify.yaml) |
| loon | `loon/spotify/spotify/spotify.list` | 62 | 1960 | `e51a09bbaa4d0d9f584c9834b25e8e5344c4a3414ab184aedcdd3dafb5f29e21` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/spotify/spotify/spotify.list) |
| mihomo | `mihomo/spotify/spotify/spotify.yaml` | 62 | 2217 | `c845951d596152f5a54c4d4ec62b95083930be840de630d86208f889f755415b` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/spotify/spotify/spotify.yaml) |
| quantumultx | `quantumultx/spotify/spotify/spotify.list` | 62 | 2336 | `4162c7a044659cfac69655ced21a75de2cea81bea10785d7e7c1a1717b28f3b9` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/spotify/spotify/spotify.list) |
| shadowrocket | `shadowrocket/spotify/spotify/spotify.list` | 62 | 1960 | `e51a09bbaa4d0d9f584c9834b25e8e5344c4a3414ab184aedcdd3dafb5f29e21` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/spotify/spotify/spotify.list) |
| singbox | `singbox/spotify/spotify/spotify.json` | 0 | 2071 | `edab95120d42d8d1df52eedacfb3e57b3694593a2b90c66cdae08c898b9ae23f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/spotify/spotify/spotify.json) |
| surge | `surge/spotify/spotify/spotify.list` | 62 | 1960 | `e51a09bbaa4d0d9f584c9834b25e8e5344c4a3414ab184aedcdd3dafb5f29e21` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/spotify/spotify/spotify.list) |

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