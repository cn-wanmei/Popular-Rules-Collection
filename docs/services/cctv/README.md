<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/tabler/service.svg" alt="CCTV 图标" width="72" height="72">

# CCTV — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `cctv_aggregate` |
| 类型 | provider_aggregate |
| Provider | `cctv` |
| 语义规则数量 | **44** |
| 语义 SHA-256 | `aab05d7ba14510fc6af2708a392a7bc884749e44c18b28e417843c94f24a5204` |
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
| egern | `egern/cctv/cctv.yaml` | 44 | 964 | `e33ce9610e6b31d3b17acbb8a4c73df046c6af3040adac4d38166001e5449b0d` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/cctv/cctv.yaml) |
| loon | `loon/cctv/cctv.list` | 44 | 1297 | `f6ea7a00625b63d888f9ef876bea437f22f4210b1f27e0311b6f6882ae4e11f7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/cctv/cctv.list) |
| mihomo | `mihomo/cctv/cctv.yaml` | 44 | 1482 | `b036fa84d3e79dbd98b5a20a6ad790c20a6cd7ab05ec4b6971d43378ca6a92f7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/cctv/cctv.yaml) |
| quantumultx | `quantumultx/cctv/cctv.list` | 44 | 1561 | `e96a9aad45e672bb6cf452fc372f676ba20e1504748f7d56a32ea66bc06f28ae` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/cctv/cctv.list) |
| shadowrocket | `shadowrocket/cctv/cctv.list` | 44 | 1297 | `f6ea7a00625b63d888f9ef876bea437f22f4210b1f27e0311b6f6882ae4e11f7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/cctv/cctv.list) |
| singbox | `singbox/cctv/cctv.json` | 0 | 1246 | `8b9c35f9efbd81b71d9fd50e5be51b094293b2957e72dcc918cd0b560be473a6` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/cctv/cctv.json) |
| surge | `surge/cctv/cctv.list` | 44 | 1297 | `f6ea7a00625b63d888f9ef876bea437f22f4210b1f27e0311b6f6882ae4e11f7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/cctv/cctv.list) |

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