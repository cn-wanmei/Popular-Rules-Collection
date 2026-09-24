<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/heroicons/service.svg" alt="Hulu 图标" width="72" height="72">

# Hulu — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `hulu` |
| 类型 | service |
| Provider | `disney` |
| 语义规则数量 | **59** |
| 语义 SHA-256 | `1b3192151389f53debae5b449000173ce5f7bcd485d1305a035db053149a8455` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**heroicons semantic fallback**

- Style：`heroicons`
- Identity：`semantic.fallback.heroicons`
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/heroicons/service.svg`
- 该图标用于覆盖缺失身份，不代表官方品牌 Logo。

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/disney/hulu/hulu.yaml` | 58 | 1231 | `a0f66374f9b5eb6531fad3d0093edfb3af671196f67b38821218699e621406c4` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/disney/hulu/hulu.yaml) |
| loon | `loon/disney/hulu/hulu.list` | 58 | 1657 | `a6f7d8b97f4989ad905b43e4ccdb382893b2c395ca66a587cee7058f3ee005f6` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/disney/hulu/hulu.list) |
| mihomo | `mihomo/disney/hulu/hulu.yaml` | 58 | 1898 | `d75bdf08cfe92ca66dad36c74f9c3e35190a57e9197507ea5fd84a57af75e41f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/disney/hulu/hulu.yaml) |
| quantumultx | `quantumultx/disney/hulu/hulu.list` | 58 | 2005 | `ae4798c9884b1c66c2a6974a98ba9d4e909c49254884f0c01839b1aa61ac3bb6` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/disney/hulu/hulu.list) |
| shadowrocket | `shadowrocket/disney/hulu/hulu.list` | 58 | 1657 | `a6f7d8b97f4989ad905b43e4ccdb382893b2c395ca66a587cee7058f3ee005f6` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/disney/hulu/hulu.list) |
| singbox | `singbox/disney/hulu/hulu.json` | 0 | 1597 | `33b96c064840f010b4c68e3fa4dcb2cbb44187caaa45fd5b5ffa72d738cce17f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/disney/hulu/hulu.json) |
| surge | `surge/disney/hulu/hulu.list` | 58 | 1657 | `a6f7d8b97f4989ad905b43e4ccdb382893b2c395ca66a587cee7058f3ee005f6` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/disney/hulu/hulu.list) |

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