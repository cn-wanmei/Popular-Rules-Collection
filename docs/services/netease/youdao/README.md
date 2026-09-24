<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/remix/service.svg" alt="Youdao 图标" width="72" height="72">

# Youdao — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `youdao` |
| 类型 | service |
| Provider | `netease` |
| 语义规则数量 | **15** |
| 语义 SHA-256 | `04f99b347db062770543ce638bcecd53cd0d03062757dbd817b34c30787db064` |
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
| egern | `egern/netease/youdao/youdao.yaml` | 15 | 349 | `919cf1cd941d4f28bc0af0af012134b2504a203268745ea03e4658e9f2df96f2` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/netease/youdao/youdao.yaml) |
| loon | `loon/netease/youdao/youdao.list` | 15 | 450 | `ce8b995aa786e698fba3c46475eafea704e2daf6a6e19a54d3112f6cd2a0024a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/netease/youdao/youdao.list) |
| mihomo | `mihomo/netease/youdao/youdao.yaml` | 15 | 519 | `8cf60a115b7de674dc559239185b29defb25c1f1730b429e75faf93c0c9edd7e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/netease/youdao/youdao.yaml) |
| quantumultx | `quantumultx/netease/youdao/youdao.list` | 15 | 540 | `e62f1e3642954bcdfdb6730934b4b49d3ea7c8c31751562017275e01dcfd5eba` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/netease/youdao/youdao.list) |
| shadowrocket | `shadowrocket/netease/youdao/youdao.list` | 15 | 450 | `ce8b995aa786e698fba3c46475eafea704e2daf6a6e19a54d3112f6cd2a0024a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/netease/youdao/youdao.list) |
| singbox | `singbox/netease/youdao/youdao.json` | 0 | 486 | `491a41d6ee6c96cef455478afeff5dc501e79b5bb0e38f9ec6d2752bd4484afd` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/netease/youdao/youdao.json) |
| surge | `surge/netease/youdao/youdao.list` | 15 | 450 | `ce8b995aa786e698fba3c46475eafea704e2daf6a6e19a54d3112f6cd2a0024a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/netease/youdao/youdao.list) |

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