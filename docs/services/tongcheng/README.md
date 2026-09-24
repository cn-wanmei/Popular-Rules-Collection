<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/bootstrap/service.svg" alt="Tongcheng 图标" width="72" height="72">

# Tongcheng — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `tongcheng_aggregate` |
| 类型 | provider_aggregate |
| Provider | `tongcheng` |
| 语义规则数量 | **8** |
| 语义 SHA-256 | `68754f5eaac0967f05399439637c517b4a150a84595d7623181a13e67d2e5ee1` |
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
| egern | `egern/tongcheng/tongcheng.yaml` | 8 | 148 | `e4f1dbf77e27328bcf86ec19d9eb962f5ebc42508c464ca069add3325b1c6f93` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/tongcheng/tongcheng.yaml) |
| loon | `loon/tongcheng/tongcheng.list` | 8 | 193 | `6f62cb5711ce7ae2506704899e1732d17ba237d5e29cdcb2851a9857769289e7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/tongcheng/tongcheng.list) |
| mihomo | `mihomo/tongcheng/tongcheng.yaml` | 8 | 234 | `0f7b1577d32e94d647d3e0d208f7877a8f423b5341363def394ad4e99c7ae808` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/tongcheng/tongcheng.yaml) |
| quantumultx | `quantumultx/tongcheng/tongcheng.list` | 8 | 241 | `a8b838bf1e935ded9e2bff417e03d63f109c5b62c24481aad4e2b2bb6b7d3689` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/tongcheng/tongcheng.list) |
| shadowrocket | `shadowrocket/tongcheng/tongcheng.list` | 8 | 193 | `6f62cb5711ce7ae2506704899e1732d17ba237d5e29cdcb2851a9857769289e7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/tongcheng/tongcheng.list) |
| singbox | `singbox/tongcheng/tongcheng.json` | 0 | 250 | `40aba9b0a4573eef9894aa5abf01c8da88c7a7d859f88b6cbe84dc3669aa9bfa` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/tongcheng/tongcheng.json) |
| surge | `surge/tongcheng/tongcheng.list` | 8 | 193 | `6f62cb5711ce7ae2506704899e1732d17ba237d5e29cdcb2851a9857769289e7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/tongcheng/tongcheng.list) |

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