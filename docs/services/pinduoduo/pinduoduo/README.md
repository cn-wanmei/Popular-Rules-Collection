<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/phosphor/service.svg" alt="Pinduoduo 图标" width="72" height="72">

# Pinduoduo — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `pinduoduo` |
| 类型 | service |
| Provider | `pinduoduo` |
| 语义规则数量 | **3** |
| 语义 SHA-256 | `defe32c7738cf99a6ce073b1dddfad4adcfb2f9c7c6c7f4061a2376a3f50424f` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**phosphor semantic fallback**

- Style：`phosphor`
- Identity：`semantic.fallback.phosphor`
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/phosphor/service.svg`
- 该图标用于覆盖缺失身份，不代表官方品牌 Logo。

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/pinduoduo/pinduoduo/pinduoduo.yaml` | 3 | 76 | `6d7589dc9a0cd94064c0d0290da584838c1806b92f35f69be5818be7cd664106` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/pinduoduo/pinduoduo/pinduoduo.yaml) |
| loon | `loon/pinduoduo/pinduoduo/pinduoduo.list` | 3 | 81 | `5c72d6b5f95cb88c69ce2276d709310f46700a565f03b4a05485a1e1e9810fec` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/pinduoduo/pinduoduo/pinduoduo.list) |
| mihomo | `mihomo/pinduoduo/pinduoduo/pinduoduo.yaml` | 3 | 102 | `fcb2c2acd00029a7f875b6a4d5d8baa64f64ee20166c14926a76297362280f14` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/pinduoduo/pinduoduo/pinduoduo.yaml) |
| quantumultx | `quantumultx/pinduoduo/pinduoduo/pinduoduo.list` | 3 | 99 | `860e7c1a932074a6d0b7cf8c3fb4319ccc2fbb3ab3f06a21038c6e5112598267` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/pinduoduo/pinduoduo/pinduoduo.list) |
| shadowrocket | `shadowrocket/pinduoduo/pinduoduo/pinduoduo.list` | 3 | 81 | `5c72d6b5f95cb88c69ce2276d709310f46700a565f03b4a05485a1e1e9810fec` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/pinduoduo/pinduoduo/pinduoduo.list) |
| singbox | `singbox/pinduoduo/pinduoduo/pinduoduo.json` | 0 | 153 | `dcaf78dc6d8642c3fcb55b145e733713055f07f7fc3e22ff237da362b639af53` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/pinduoduo/pinduoduo/pinduoduo.json) |
| surge | `surge/pinduoduo/pinduoduo/pinduoduo.list` | 3 | 81 | `5c72d6b5f95cb88c69ce2276d709310f46700a565f03b4a05485a1e1e9810fec` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/pinduoduo/pinduoduo/pinduoduo.list) |

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