<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/facebook.png" alt="Facebook 图标" width="72" height="72">

# Facebook — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `facebook` |
| 类型 | service |
| Provider | `meta` |
| 语义规则数量 | **576** |
| 语义 SHA-256 | `1fb047ab1485727c0acc6194e70704966b8761dc64ca0f4cc91f439bec38014d` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.facebook`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/facebook.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/meta/facebook/facebook.yaml` | 1363 | 30009 | `3680e5b56bff9728102192c7153853637a48ccb7b295a493547f8a26a2c85ebf` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/meta/facebook/facebook.yaml) |
| loon | `loon/meta/facebook/facebook.list` | 1363 | 40706 | `030095761950eae88b358548893facd9426663e7f60e3020efe77eb0207910dc` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/meta/facebook/facebook.list) |
| mihomo | `mihomo/meta/facebook/facebook.yaml` | 1363 | 46167 | `2d5dbef87d02e3a4ab66ef158f231a8f9f433efad7d8ab07853803357351b452` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/meta/facebook/facebook.yaml) |
| quantumultx | `quantumultx/meta/facebook/facebook.list` | 1363 | 48930 | `55852e17b1f7fb7054cda0028f39e796f5ff1c36b34f8e1cb245b53c79a5c6e9` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/meta/facebook/facebook.list) |
| shadowrocket | `shadowrocket/meta/facebook/facebook.list` | 1363 | 40706 | `030095761950eae88b358548893facd9426663e7f60e3020efe77eb0207910dc` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/meta/facebook/facebook.list) |
| singbox | `singbox/meta/facebook/facebook.json` | 0 | 36928 | `c2746e8b11659018274be2471e89d0894bbc6c839c581430ff9a6ddef86b2f5f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/meta/facebook/facebook.json) |
| surge | `surge/meta/facebook/facebook.list` | 1363 | 40706 | `030095761950eae88b358548893facd9426663e7f60e3020efe77eb0207910dc` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/meta/facebook/facebook.list) |

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