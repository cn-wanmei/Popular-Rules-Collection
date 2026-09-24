<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/bootstrap/service.svg" alt="China Everbright Bank 图标" width="72" height="72">

# China Everbright Bank — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `ceb` |
| 类型 | service |
| Provider | `ceb` |
| 语义规则数量 | **15** |
| 语义 SHA-256 | `c225b14741d167df7bc575f7f9aae149d39cce9b5eb90cc9ebb9fca82f897921` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**bootstrap semantic fallback**

- Style：`bootstrap`
- Identity：`semantic.fallback.bootstrap`
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/bootstrap/service.svg`
- 该图标用于覆盖缺失身份，不代表官方品牌 Logo。

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/ceb/ceb/ceb.yaml` | 15 | 303 | `e830ceae173a6f2308796734c3fbc52ef0b09f97341dfa9ccb6665128457bf98` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/ceb/ceb/ceb.yaml) |
| loon | `loon/ceb/ceb/ceb.list` | 15 | 404 | `374e4ce590adf33b251507933cbe1c549c65159c122f95780970e969037add2c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/ceb/ceb/ceb.list) |
| mihomo | `mihomo/ceb/ceb/ceb.yaml` | 15 | 473 | `ce3f66bc3172835e79e1c62b5a81a627b9f7333e7272bf8d2610dc6ca046b19a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/ceb/ceb/ceb.yaml) |
| quantumultx | `quantumultx/ceb/ceb/ceb.list` | 15 | 494 | `d0d0993b4da4b3b4c2a761c4d3a65255425403ee3ec501db7a3b61302f2f4c84` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/ceb/ceb/ceb.list) |
| shadowrocket | `shadowrocket/ceb/ceb/ceb.list` | 15 | 404 | `374e4ce590adf33b251507933cbe1c549c65159c122f95780970e969037add2c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/ceb/ceb/ceb.list) |
| singbox | `singbox/ceb/ceb/ceb.json` | 0 | 440 | `05fe1c53a961e58514ea2bc90094e94c6c08df1a46693f28c8209a5fa1b5de5e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/ceb/ceb/ceb.json) |
| surge | `surge/ceb/ceb/ceb.list` | 15 | 404 | `374e4ce590adf33b251507933cbe1c549c65159c122f95780970e969037add2c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/ceb/ceb/ceb.list) |

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