<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/tabler/service.svg" alt="UnionPay 图标" width="72" height="72">

# UnionPay — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `unionpay` |
| 类型 | service |
| Provider | `unionpay` |
| 语义规则数量 | **16** |
| 语义 SHA-256 | `3cbbe321186965e7ea04b56fbea849aa72fd27db627a38c8689e27cb78b5edf0` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**tabler semantic fallback**

- Style：`tabler`
- Identity：`semantic.fallback.tabler`
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/tabler/service.svg`
- 该图标用于覆盖缺失身份，不代表官方品牌 Logo。

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/unionpay/unionpay/unionpay.yaml` | 16 | 348 | `b2a646c14bc080f27cb2b534598cfa0a07235a77d724c10a1daf3388497341aa` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/unionpay/unionpay/unionpay.yaml) |
| loon | `loon/unionpay/unionpay/unionpay.list` | 16 | 457 | `0debe3092e2e14067698e9a90bc7fc143a255d41c01d886121ddba067003831f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/unionpay/unionpay/unionpay.list) |
| mihomo | `mihomo/unionpay/unionpay/unionpay.yaml` | 16 | 530 | `9ca101fee251cb8068d98e5bf92654c734914863350c496acc857293cd4068ac` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/unionpay/unionpay/unionpay.yaml) |
| quantumultx | `quantumultx/unionpay/unionpay/unionpay.list` | 16 | 553 | `03efad8a159c36fd79cc579b1fd53d86390444403993bb631b9cff90d0631b58` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/unionpay/unionpay/unionpay.list) |
| shadowrocket | `shadowrocket/unionpay/unionpay/unionpay.list` | 16 | 457 | `0debe3092e2e14067698e9a90bc7fc143a255d41c01d886121ddba067003831f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/unionpay/unionpay/unionpay.list) |
| singbox | `singbox/unionpay/unionpay/unionpay.json` | 0 | 490 | `9130395bb7f5b939a81b00c7e400986bda7c94f2af0d9d2bfae866c7ce2d60ef` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/unionpay/unionpay/unionpay.json) |
| surge | `surge/unionpay/unionpay/unionpay.list` | 16 | 457 | `0debe3092e2e14067698e9a90bc7fc143a255d41c01d886121ddba067003831f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/unionpay/unionpay/unionpay.list) |

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