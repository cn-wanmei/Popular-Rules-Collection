<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/atlassian.png" alt="Atlassian 图标" width="72" height="72">

# Atlassian — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `atlassian` |
| 类型 | provider_aggregate |
| Provider | `atlassian` |
| 语义规则数量 | **11** |
| 语义 SHA-256 | `eae6f0c72a1c6eab6d496e65bf0bbb2bbfb562ab0eb3f117c9b3e438a997ba2c` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.atlassian`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/atlassian.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/atlassian/atlassian.yaml` | 11 | 230 | `c52fde55245508e12952f1cf42483f17b57773d4dbe483783118345f65299afd` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/atlassian/atlassian.yaml) |
| loon | `loon/atlassian/atlassian.list` | 11 | 299 | `bd2a8be185306fbd9ed278ce7f9d7fe541e488dae72d708c9045906260b8d0da` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/atlassian/atlassian.list) |
| mihomo | `mihomo/atlassian/atlassian.yaml` | 11 | 352 | `2416d458e94519b248bd029edff9b33e25607e0d26daf47da88f3c8bc63f5289` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/atlassian/atlassian.yaml) |
| quantumultx | `quantumultx/atlassian/atlassian.list` | 11 | 365 | `3a0a917523182ae95557bdaed122f788702794f307d7246b5ce2163cb7b3bdbc` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/atlassian/atlassian.list) |
| shadowrocket | `shadowrocket/atlassian/atlassian.list` | 11 | 299 | `bd2a8be185306fbd9ed278ce7f9d7fe541e488dae72d708c9045906260b8d0da` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/atlassian/atlassian.list) |
| singbox | `singbox/atlassian/atlassian.json` | 0 | 347 | `8736b41c8a34799bfff6682f7c554cebbef93589fae6981e69e8bb61b29bf692` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/atlassian/atlassian.json) |
| surge | `surge/atlassian/atlassian.list` | 11 | 299 | `bd2a8be185306fbd9ed278ce7f9d7fe541e488dae72d708c9045906260b8d0da` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/atlassian/atlassian.list) |

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