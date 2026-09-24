<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/chinaunicom.png" alt="China Unicom 图标" width="72" height="72">

# China Unicom — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `chinaunicom_aggregate` |
| 类型 | provider_aggregate |
| Provider | `chinaunicom` |
| 语义规则数量 | **34** |
| 语义 SHA-256 | `19d41c1363a6caf6a1d531b81639467271bae7fb5c37e075f8114aa9eeaf15c5` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`semantic.chinaunicom`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/chinaunicom.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/chinaunicom/chinaunicom.yaml` | 34 | 694 | `22ff6f25caa765ca2439db3ca4f5629726cfd506b3a2a8198b723815f1c5b51b` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/chinaunicom/chinaunicom.yaml) |
| loon | `loon/chinaunicom/chinaunicom.list` | 34 | 928 | `bacce6f755aaf0e8e2d03c190d952793282a2f65816dba239a93f282fb7e17f0` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/chinaunicom/chinaunicom.list) |
| mihomo | `mihomo/chinaunicom/chinaunicom.yaml` | 34 | 1073 | `23af650b9a78c0eca518ab11daae677db8230a20f06b685a6b0b17e0468ae72f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/chinaunicom/chinaunicom.yaml) |
| quantumultx | `quantumultx/chinaunicom/chinaunicom.list` | 34 | 1134 | `a2b3944dcc9153d3eed6102f674eb7db99c97a515195f40591ad8a277abec454` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/chinaunicom/chinaunicom.list) |
| shadowrocket | `shadowrocket/chinaunicom/chinaunicom.list` | 34 | 928 | `bacce6f755aaf0e8e2d03c190d952793282a2f65816dba239a93f282fb7e17f0` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/chinaunicom/chinaunicom.list) |
| singbox | `singbox/chinaunicom/chinaunicom.json` | 0 | 940 | `93a385c44ef6b2cba480699f27386778a75c98967363a8011cac876a33b90132` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/chinaunicom/chinaunicom.json) |
| surge | `surge/chinaunicom/chinaunicom.list` | 34 | 928 | `bacce6f755aaf0e8e2d03c190d952793282a2f65816dba239a93f282fb7e17f0` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/chinaunicom/chinaunicom.list) |

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