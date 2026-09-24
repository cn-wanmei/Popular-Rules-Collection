<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/gitlab.png" alt="GitLab 图标" width="72" height="72">

# GitLab — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `gitlab_aggregate` |
| 类型 | provider_aggregate |
| Provider | `gitlab` |
| 语义规则数量 | **6** |
| 语义 SHA-256 | `3105b121f0fca317e696779133748627621e6c1af9e93213643680ea8973ef5b` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.gitlab`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/gitlab.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/gitlab/gitlab.yaml` | 6 | 166 | `ecab3b8eeea31105b5bb55c89b776bf20143988cedf68b90867ae85cc2f663c8` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/gitlab/gitlab.yaml) |
| loon | `loon/gitlab/gitlab.list` | 6 | 195 | `6e020ca1c8bae17f34c4c8ed8408e3ed9e885bf29f65c2edae192b06d57efd10` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/gitlab/gitlab.list) |
| mihomo | `mihomo/gitlab/gitlab.yaml` | 6 | 228 | `b936af06dc88c3df622cb78e0a41dfcc4c2a3d92fcac8680a38f37cd542080aa` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/gitlab/gitlab.yaml) |
| quantumultx | `quantumultx/gitlab/gitlab.list` | 6 | 231 | `9c5cdd11940a7b4c9987193a7c6e285751cb0b68b140f1941965d387b1443af9` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/gitlab/gitlab.list) |
| shadowrocket | `shadowrocket/gitlab/gitlab.list` | 6 | 195 | `6e020ca1c8bae17f34c4c8ed8408e3ed9e885bf29f65c2edae192b06d57efd10` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/gitlab/gitlab.list) |
| singbox | `singbox/gitlab/gitlab.json` | 0 | 258 | `d83ea2d31394f2a8787b13923bad99d1e4c42cc61a0a2967591d130e3e1f47fe` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/gitlab/gitlab.json) |
| surge | `surge/gitlab/gitlab.list` | 6 | 195 | `6e020ca1c8bae17f34c4c8ed8408e3ed9e885bf29f65c2edae192b06d57efd10` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/gitlab/gitlab.list) |

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