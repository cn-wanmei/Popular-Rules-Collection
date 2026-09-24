<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/tabler/service.svg" alt="Tencent Meeting 图标" width="72" height="72">

# Tencent Meeting — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `tencentmeeting` |
| 类型 | service |
| Provider | `tencent` |
| 语义规则数量 | **3** |
| 语义 SHA-256 | `26ee0a1f0380f15b9132683e97e5a2b5ac3476a97370dece8bb67f2e35cdb708` |
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
| egern | `egern/tencent/tencentmeeting/tencentmeeting.yaml` | 3 | 108 | `978a336576e93243dd54194e2d93a6bf514457f5f603864163e81829ee74a248` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/tencent/tencentmeeting/tencentmeeting.yaml) |
| loon | `loon/tencent/tencentmeeting/tencentmeeting.list` | 3 | 113 | `38e9aa5e60f537aad392eba3234f1d1adbd63bfa6e027b4d35028fb37f9fa861` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/tencent/tencentmeeting/tencentmeeting.list) |
| mihomo | `mihomo/tencent/tencentmeeting/tencentmeeting.yaml` | 3 | 134 | `fa31a78a1963d44f5f6671fae7d0fae025ebe586ebbc845ea85de2e718d142e5` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/tencent/tencentmeeting/tencentmeeting.yaml) |
| quantumultx | `quantumultx/tencent/tencentmeeting/tencentmeeting.list` | 3 | 131 | `72ddc48c4f66b1fefe9455e9a0a678151ae7326c0b61b11dfa6d4871104e5768` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/tencent/tencentmeeting/tencentmeeting.list) |
| shadowrocket | `shadowrocket/tencent/tencentmeeting/tencentmeeting.list` | 3 | 113 | `38e9aa5e60f537aad392eba3234f1d1adbd63bfa6e027b4d35028fb37f9fa861` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/tencent/tencentmeeting/tencentmeeting.list) |
| singbox | `singbox/tencent/tencentmeeting/tencentmeeting.json` | 0 | 185 | `0d022cc07c90197b4c80bd464fbdad2255a9343b145701a5e97e342f82f604bb` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/tencent/tencentmeeting/tencentmeeting.json) |
| surge | `surge/tencent/tencentmeeting/tencentmeeting.list` | 3 | 113 | `38e9aa5e60f537aad392eba3234f1d1adbd63bfa6e027b4d35028fb37f9fa861` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/tencent/tencentmeeting/tencentmeeting.list) |

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