<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/phosphor/service.svg" alt="PPTV 图标" width="72" height="72">

# PPTV — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `pptv` |
| 类型 | service |
| Provider | `pptv` |
| 语义规则数量 | **19** |
| 语义 SHA-256 | `d1d71c83f19b7ff3ab5ca8d68261e7b59b33edb1fbdeae075b23c0b8b59fb024` |
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
| egern | `egern/pptv/pptv/pptv.yaml` | 19 | 342 | `b83ee04c66f8a783d9849109b757340742677977757603249f4a50ee2ff739aa` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/pptv/pptv/pptv.yaml) |
| loon | `loon/pptv/pptv/pptv.list` | 19 | 475 | `4020aea285ee2b4ff8785b66b2757e2854a7732d148fe31efa94d3e7a09b9f44` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/pptv/pptv/pptv.list) |
| mihomo | `mihomo/pptv/pptv/pptv.yaml` | 19 | 560 | `412a5e7de1f5bbb0f5c8ee831804afa9c43486a07b36e80ff9e8ba43dd9f1747` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/pptv/pptv/pptv.yaml) |
| quantumultx | `quantumultx/pptv/pptv/pptv.list` | 19 | 589 | `bbad6bf9967ec4c6b0ab7501edd3d9d9c9d2e0a161b3d03d7051dd48e9d47953` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/pptv/pptv/pptv.list) |
| shadowrocket | `shadowrocket/pptv/pptv/pptv.list` | 19 | 475 | `4020aea285ee2b4ff8785b66b2757e2854a7732d148fe31efa94d3e7a09b9f44` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/pptv/pptv/pptv.list) |
| singbox | `singbox/pptv/pptv/pptv.json` | 0 | 499 | `bfdfd797cac15ceb0dc85a9038521bd6c3514491cf9a12b24d613458cc140db8` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/pptv/pptv/pptv.json) |
| surge | `surge/pptv/pptv/pptv.list` | 19 | 475 | `4020aea285ee2b4ff8785b66b2757e2854a7732d148fe31efa94d3e7a09b9f44` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/pptv/pptv/pptv.list) |

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