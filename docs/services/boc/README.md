<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/remix/service.svg" alt="Bank of China 图标" width="72" height="72">

# Bank of China — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `boc_aggregate` |
| 类型 | provider_aggregate |
| Provider | `boc` |
| 语义规则数量 | **22** |
| 语义 SHA-256 | `f9d5e6d481a0339b2c5bc342c1589ad516676cb16802d12a86c9ff458d3e1856` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**remix semantic fallback**

- Style：`remix`
- Identity：`semantic.fallback.remix`
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/remix/service.svg`
- 该图标用于覆盖缺失身份，不代表官方品牌 Logo。

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/boc/boc.yaml` | 22 | 455 | `6b4cb4df2876e769bdea27247341fae6f0666f9a5ac9c962a2f5a280c5e6c308` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/boc/boc.yaml) |
| loon | `loon/boc/boc.list` | 22 | 612 | `48fe6f824eb09ab0e996464d8f530bf8224ee6a6c13d47c6c06c68ed55538cc9` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/boc/boc.list) |
| mihomo | `mihomo/boc/boc.yaml` | 22 | 709 | `fadb68309e0011571737563da38fb4a04eb511da33aa33ac7eb46128023fafcc` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/boc/boc.yaml) |
| quantumultx | `quantumultx/boc/boc.list` | 22 | 744 | `dd288631b98026ad0ea66e8ba10e84af8d2a71c02ea79cb629a8713bd204ad5a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/boc/boc.list) |
| shadowrocket | `shadowrocket/boc/boc.list` | 22 | 612 | `48fe6f824eb09ab0e996464d8f530bf8224ee6a6c13d47c6c06c68ed55538cc9` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/boc/boc.list) |
| singbox | `singbox/boc/boc.json` | 0 | 627 | `293049562548c83203413b297342d574401ce34aefea2a8f481bf3251cb28bb5` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/boc/boc.json) |
| surge | `surge/boc/boc.list` | 22 | 612 | `48fe6f824eb09ab0e996464d8f530bf8224ee6a6c13d47c6c06c68ed55538cc9` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/boc/boc.list) |

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