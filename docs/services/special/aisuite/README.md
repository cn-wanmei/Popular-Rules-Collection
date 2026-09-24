<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/lucide/service.svg" alt="AI Suite 图标" width="72" height="72">

# AI Suite — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `aisuite` |
| 类型 | service |
| Provider | `special` |
| 语义规则数量 | **96** |
| 语义 SHA-256 | `36f5f50ab77f780ccecbad17eb3837396e5506da4e489c6a3a07a4a7c0885d85` |
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
| egern | `egern/special/aisuite/aisuite.yaml` | 96 | 2423 | `b6e17be65778f8712502f66351e5eae39a04b9dc57bb4959b6f78a2e0e6d2280` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/special/aisuite/aisuite.yaml) |
| loon | `loon/special/aisuite/aisuite.list` | 96 | 2980 | `2f64e09761073b05074c0b735731356b558b8c7efe04dce4e9e0449284f48181` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/special/aisuite/aisuite.list) |
| mihomo | `mihomo/special/aisuite/aisuite.yaml` | 96 | 3373 | `b05cfda453274c4f0ddfb7e380344d85bb8185ac492fc42465b63fd0a5205671` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/special/aisuite/aisuite.yaml) |
| quantumultx | `quantumultx/special/aisuite/aisuite.list` | 96 | 3556 | `66ef0da7f779d60ac2d84e0e2fc170907f9561147648aac5a905b01e80913326` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/special/aisuite/aisuite.list) |
| shadowrocket | `shadowrocket/special/aisuite/aisuite.list` | 96 | 2980 | `2f64e09761073b05074c0b735731356b558b8c7efe04dce4e9e0449284f48181` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/special/aisuite/aisuite.list) |
| singbox | `singbox/special/aisuite/aisuite.json` | 0 | 2993 | `775a0aba7e0557fa5341264272751d27c978498d16caa834f73e64c3e1672157` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/special/aisuite/aisuite.json) |
| surge | `surge/special/aisuite/aisuite.list` | 96 | 2980 | `2f64e09761073b05074c0b735731356b558b8c7efe04dce4e9e0449284f48181` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/special/aisuite/aisuite.list) |

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