<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/remix/service.svg" alt="DouYu 图标" width="72" height="72">

# DouYu — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `douyu_aggregate` |
| 类型 | provider_aggregate |
| Provider | `douyu` |
| 语义规则数量 | **13** |
| 语义 SHA-256 | `20de7c3e00ef4e29801d9056de0e2f5bc21fd54d85eef08c8f9885edbb4494a2` |
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
| egern | `egern/douyu/douyu.yaml` | 13 | 254 | `15e0b2b1b5b349118178b57d1ef0d0427544757077c404fe99fb476aa4cf400d` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/douyu/douyu.yaml) |
| loon | `loon/douyu/douyu.list` | 13 | 339 | `78bdbd4ea6e87b616c63a03f96a5cff22c12eaa67bf8a74ad4bbcf74692bd461` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/douyu/douyu.list) |
| mihomo | `mihomo/douyu/douyu.yaml` | 13 | 400 | `d433d401b3dad834dc79ed3f0ae1af175ecd9f241fb8bf4de2c7f45a406945ea` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/douyu/douyu.yaml) |
| quantumultx | `quantumultx/douyu/douyu.list` | 13 | 417 | `48be459ace7f63cf36ce9b693eb94a67beb205bc6eace100f27b5ce57fd30d2e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/douyu/douyu.list) |
| shadowrocket | `shadowrocket/douyu/douyu.list` | 13 | 339 | `78bdbd4ea6e87b616c63a03f96a5cff22c12eaa67bf8a74ad4bbcf74692bd461` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/douyu/douyu.list) |
| singbox | `singbox/douyu/douyu.json` | 0 | 381 | `53403090f0714e3d96edcb384319b2420d57da4a0cb4a2309074520365cc3196` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/douyu/douyu.json) |
| surge | `surge/douyu/douyu.list` | 13 | 339 | `78bdbd4ea6e87b616c63a03f96a5cff22c12eaa67bf8a74ad4bbcf74692bd461` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/douyu/douyu.list) |

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