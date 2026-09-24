<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/speedtest.png" alt="Speedtest 图标" width="72" height="72">

# Speedtest — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `speedtest` |
| 类型 | service |
| Provider | `ookla` |
| 语义规则数量 | **5** |
| 语义 SHA-256 | `8b05ad3958c722577cc915f93ebff010cb77199b1250fd0bfbd6abdbaab92c34` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**品牌 / 已有身份图标**

- Identity：`brand.speedtest`
- 来源：Current V3 已发布图标资产
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/speedtest.png`

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/ookla/speedtest/speedtest.yaml` | 5 | 139 | `8fc7f8174ca2c13dad1741838404a5940d8d3b57a13ba5d272f0937c0a8335fc` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/ookla/speedtest/speedtest.yaml) |
| loon | `loon/ookla/speedtest/speedtest.list` | 5 | 141 | `ec14ed49c2c4c67f5d9039fb6bd050c84e853139aeda81f81087242b846f03e0` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/ookla/speedtest/speedtest.list) |
| mihomo | `mihomo/ookla/speedtest/speedtest.yaml` | 5 | 170 | `0318fdd30e2df462758c7f930d69247ce1a39c5bfbd6ef4517e0e60a26fe08ef` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/ookla/speedtest/speedtest.yaml) |
| quantumultx | `quantumultx/ookla/speedtest/speedtest.list` | 5 | 171 | `7c5e6ab648310a980eabfce602592f187d1ec3f9393cb6e96aa8bd06e7bf8deb` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/ookla/speedtest/speedtest.list) |
| shadowrocket | `shadowrocket/ookla/speedtest/speedtest.list` | 5 | 141 | `ec14ed49c2c4c67f5d9039fb6bd050c84e853139aeda81f81087242b846f03e0` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/ookla/speedtest/speedtest.list) |
| singbox | `singbox/ookla/speedtest/speedtest.json` | 0 | 240 | `b1f5c2ccee89cb1f1cf1d462a3d16dec8804c78893045c8a2bff16933b78e03c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/ookla/speedtest/speedtest.json) |
| surge | `surge/ookla/speedtest/speedtest.list` | 5 | 141 | `ec14ed49c2c4c67f5d9039fb6bd050c84e853139aeda81f81087242b846f03e0` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/ookla/speedtest/speedtest.list) |

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