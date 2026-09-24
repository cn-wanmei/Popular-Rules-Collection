<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/material-symbols/service.svg" alt="Industrial and Commercial Bank of China 图标" width="72" height="72">

# Industrial and Commercial Bank of China — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `icbc_aggregate` |
| 类型 | provider_aggregate |
| Provider | `icbc` |
| 语义规则数量 | **58** |
| 语义 SHA-256 | `5d197fa67d758d57e1efcf6a11cf4ba04dc1ffad2328b2b61c8c86e8f12afdc5` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**material-symbols semantic fallback**

- Style：`material-symbols`
- Identity：`semantic.fallback.material-symbols`
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/material-symbols/service.svg`
- 该图标用于覆盖缺失身份，不代表官方品牌 Logo。

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/icbc/icbc.yaml` | 58 | 1121 | `017b86c5a6a5c4a301fe2e2d8ec7524c7e7e0fd849a2d7f609eb97b1748eb2ea` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/icbc/icbc.yaml) |
| loon | `loon/icbc/icbc.list` | 58 | 1547 | `65bb0a2d3849646958e00633e7fec75c1bac530703e8cb8ab5655dab2dd40404` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/icbc/icbc.list) |
| mihomo | `mihomo/icbc/icbc.yaml` | 58 | 1788 | `dec9acc349cedb364bf3fdfbdd349b49647ae4bbacdde035868275b6f1727ac9` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/icbc/icbc.yaml) |
| quantumultx | `quantumultx/icbc/icbc.list` | 58 | 1895 | `9e70fb0053c8a5ad15e7808b2101b673c738afade57a6883dcb5d357f85962c1` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/icbc/icbc.list) |
| shadowrocket | `shadowrocket/icbc/icbc.list` | 58 | 1547 | `65bb0a2d3849646958e00633e7fec75c1bac530703e8cb8ab5655dab2dd40404` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/icbc/icbc.list) |
| singbox | `singbox/icbc/icbc.json` | 0 | 1487 | `577fdf1df67f339beb61ef3ad4d9ceda58d3050a7f37086007d7a6fe4a0b52cc` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/icbc/icbc.json) |
| surge | `surge/icbc/icbc.list` | 58 | 1547 | `65bb0a2d3849646958e00633e7fec75c1bac530703e8cb8ab5655dab2dd40404` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/icbc/icbc.list) |

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