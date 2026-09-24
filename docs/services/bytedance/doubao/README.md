<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/bootstrap/service.svg" alt="Doubao 图标" width="72" height="72">

# Doubao — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `doubao` |
| 类型 | service |
| Provider | `bytedance` |
| 语义规则数量 | **4** |
| 语义 SHA-256 | `6127cf2d2740f584a6dd54472436357d0d0124647a8e62ccd0b29b285c7b3908` |
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
| egern | `egern/bytedance/doubao/doubao.yaml` | 4 | 120 | `e9394dd4fa9a5f57725738b044227515a849b564bf2171cb2c832933d91e83b5` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/bytedance/doubao/doubao.yaml) |
| loon | `loon/bytedance/doubao/doubao.list` | 4 | 133 | `2ddcdb67d2b9bf06ee5d6c390f8a5092516c4cd7c4ee4ce257751606a55c9522` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/bytedance/doubao/doubao.list) |
| mihomo | `mihomo/bytedance/doubao/doubao.yaml` | 4 | 158 | `b0c3919f5f02ec740d85551f3ae806555f596b7a2441923d22725a3685228428` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/bytedance/doubao/doubao.yaml) |
| quantumultx | `quantumultx/bytedance/doubao/doubao.list` | 4 | 157 | `1c32a1a5131850eda27c2dae0a98fe9e791fee1395ce03d84ac36ec2e81d1df2` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/bytedance/doubao/doubao.list) |
| shadowrocket | `shadowrocket/bytedance/doubao/doubao.list` | 4 | 133 | `2ddcdb67d2b9bf06ee5d6c390f8a5092516c4cd7c4ee4ce257751606a55c9522` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/bytedance/doubao/doubao.list) |
| singbox | `singbox/bytedance/doubao/doubao.json` | 0 | 202 | `de8ba490b7ac06377b961f84b33a985e94e492ffcee8f34d89d26f3f50083825` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/bytedance/doubao/doubao.json) |
| surge | `surge/bytedance/doubao/doubao.list` | 4 | 133 | `2ddcdb67d2b9bf06ee5d6c390f8a5092516c4cd7c4ee4ce257751606a55c9522` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/bytedance/doubao/doubao.list) |

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