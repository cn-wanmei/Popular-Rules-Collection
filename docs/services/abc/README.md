<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/fluent/service.svg" alt="Agricultural Bank of China 图标" width="72" height="72">

# Agricultural Bank of China — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `abc_aggregate` |
| 类型 | provider_aggregate |
| Provider | `abc` |
| 语义规则数量 | **6** |
| 语义 SHA-256 | `7e626f704b43aceef59a423bf6e1e144564ad52258be9c7ae4e2837bcb62126a` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**fluent semantic fallback**

- Style：`fluent`
- Identity：`semantic.fallback.fluent`
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/fluent/service.svg`
- 该图标用于覆盖缺失身份，不代表官方品牌 Logo。

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/abc/abc.yaml` | 6 | 130 | `40bbd6c2af22ce0a4ae90dafd2b8fdf1f8a96b4d74551b4b5c4c35215f335f68` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/abc/abc.yaml) |
| loon | `loon/abc/abc.list` | 6 | 159 | `ab7eeef4fbb9ee2d4a911cc4e93ca1a7dcde8be89c40102a846ab70c527f3e90` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/abc/abc.list) |
| mihomo | `mihomo/abc/abc.yaml` | 6 | 192 | `43af8a98d19f6a250039c0b747e2110d0412a5f241a19adfb62932ea90650a49` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/abc/abc.yaml) |
| quantumultx | `quantumultx/abc/abc.list` | 6 | 195 | `1a8d79af2efd67b3ac5975b99435af57dec6e90d0a579940cfadfc50d10080ec` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/abc/abc.list) |
| shadowrocket | `shadowrocket/abc/abc.list` | 6 | 159 | `ab7eeef4fbb9ee2d4a911cc4e93ca1a7dcde8be89c40102a846ab70c527f3e90` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/abc/abc.list) |
| singbox | `singbox/abc/abc.json` | 0 | 222 | `25ce9490bd37dde1fa12610958d6d56d02efe8f5716cb6f77e431e4b0c0c0215` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/abc/abc.json) |
| surge | `surge/abc/abc.list` | 6 | 159 | `ab7eeef4fbb9ee2d4a911cc4e93ca1a7dcde8be89c40102a846ab70c527f3e90` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/abc/abc.list) |

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