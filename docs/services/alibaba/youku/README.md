<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/remix/service.svg" alt="Youku 图标" width="72" height="72">

# Youku — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `youku` |
| 类型 | service |
| Provider | `alibaba` |
| 语义规则数量 | **60** |
| 语义 SHA-256 | `f144243efce9c9ae996556f42aa61f25411ee18bee4a7133efd235bf36a26004` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**remix semantic fallback**

- Style：`remix`
- Identity：`semantic.fallback.remix`
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/remix/service.svg`
- 该图标用于覆盖缺失身份，不代表官方品牌 Logo。

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/alibaba/youku/youku.yaml` | 66 | 1392 | `520de05714c09845f65e4d65be34e996862c159f437be3fb18e73126ac64eb82` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/alibaba/youku/youku.yaml) |
| loon | `loon/alibaba/youku/youku.list` | 66 | 1882 | `897eea132a968e3b64a847a6ac1605d141dc4456973dd87706e4191303b82cde` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/alibaba/youku/youku.list) |
| mihomo | `mihomo/alibaba/youku/youku.yaml` | 66 | 2155 | `ae71d4df3311c1da958095bbcbb78c6f99f4b6112e6a3b4c86995844d8395a4d` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/alibaba/youku/youku.yaml) |
| quantumultx | `quantumultx/alibaba/youku/youku.list` | 66 | 2280 | `2ebfb0c3820b161875c20ea81c05fb01c2a4c8505a936a4269b52561f8e98566` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/alibaba/youku/youku.list) |
| shadowrocket | `shadowrocket/alibaba/youku/youku.list` | 66 | 1882 | `897eea132a968e3b64a847a6ac1605d141dc4456973dd87706e4191303b82cde` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/alibaba/youku/youku.list) |
| singbox | `singbox/alibaba/youku/youku.json` | 0 | 1798 | `ebd7d2a9cb6a3d7e562a302b3ae91cdf3ae0b6fe0d59dcb3e817e8c023e592b4` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/alibaba/youku/youku.json) |
| surge | `surge/alibaba/youku/youku.list` | 66 | 1882 | `897eea132a968e3b64a847a6ac1605d141dc4456973dd87706e4191303b82cde` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/alibaba/youku/youku.list) |

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