<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/lucide/service.svg" alt="Ximalaya 图标" width="72" height="72">

# Ximalaya — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `ximalaya_aggregate` |
| 类型 | provider_aggregate |
| Provider | `ximalaya` |
| 语义规则数量 | **5** |
| 语义 SHA-256 | `c27fa6a6e13fc00118ae0e1a39537b8f35a7b24f4285d20a18dfab3f59aa0f5e` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**lucide semantic fallback**

- Style：`lucide`
- Identity：`semantic.fallback.lucide`
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/lucide/service.svg`
- 该图标用于覆盖缺失身份，不代表官方品牌 Logo。

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/ximalaya/ximalaya.yaml` | 5 | 136 | `1fab6ddbe73b126273077d22df36d76cb45e95434450ac8ece816648e11ec47e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/ximalaya/ximalaya.yaml) |
| loon | `loon/ximalaya/ximalaya.list` | 5 | 157 | `9ea6041a2fd02aabd775ecfa1b0401a91fe38e8bb5fa9d2ea38704be46a274a7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/ximalaya/ximalaya.list) |
| mihomo | `mihomo/ximalaya/ximalaya.yaml` | 5 | 186 | `a20256c79df26df67581308c9376a4e72ea0bbe5183fbd21ffa0f887f4b2f7d1` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/ximalaya/ximalaya.yaml) |
| quantumultx | `quantumultx/ximalaya/ximalaya.list` | 5 | 187 | `3a8cbc6fef199e6a0e2c580ef0149c8a6f1a0100238bdd891800607e77f47840` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/ximalaya/ximalaya.list) |
| shadowrocket | `shadowrocket/ximalaya/ximalaya.list` | 5 | 157 | `9ea6041a2fd02aabd775ecfa1b0401a91fe38e8bb5fa9d2ea38704be46a274a7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/ximalaya/ximalaya.list) |
| singbox | `singbox/ximalaya/ximalaya.json` | 0 | 223 | `417d6d7f27cc110b8491c35ad94a6934cd0806dce0d7dbbe5b48f54c6ea3307b` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/ximalaya/ximalaya.json) |
| surge | `surge/ximalaya/ximalaya.list` | 5 | 157 | `9ea6041a2fd02aabd775ecfa1b0401a91fe38e8bb5fa9d2ea38704be46a274a7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/ximalaya/ximalaya.list) |

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