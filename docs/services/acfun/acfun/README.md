<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/remix/service.svg" alt="AcFun 图标" width="72" height="72">

# AcFun — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `acfun` |
| 类型 | service |
| Provider | `acfun` |
| 语义规则数量 | **10** |
| 语义 SHA-256 | `04edec7e594b788dab5180df4e5b785d8be9c204023cb138a30c7a9b18e19cab` |
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
| egern | `egern/acfun/acfun/acfun.yaml` | 12 | 233 | `7ec172c4221243f36ac3c619e390f18d0399ad4a797d91aee53b1ab77e265a18` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/acfun/acfun/acfun.yaml) |
| loon | `loon/acfun/acfun/acfun.list` | 12 | 310 | `09a147ebdddfb1b37e5003e2246d0193395d05822439da172bcea2420671ec3c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/acfun/acfun/acfun.list) |
| mihomo | `mihomo/acfun/acfun/acfun.yaml` | 12 | 367 | `4fbcde6ca3cbe95674c5dd198568942e20c61dafae942ba5098fa4f31dab8758` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/acfun/acfun/acfun.yaml) |
| quantumultx | `quantumultx/acfun/acfun/acfun.list` | 12 | 382 | `c0b41ad29005f42dfdaec1403febb2d91e9b719aadd327df1a1c7452e9139508` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/acfun/acfun/acfun.list) |
| shadowrocket | `shadowrocket/acfun/acfun/acfun.list` | 12 | 310 | `09a147ebdddfb1b37e5003e2246d0193395d05822439da172bcea2420671ec3c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/acfun/acfun/acfun.list) |
| singbox | `singbox/acfun/acfun/acfun.json` | 0 | 355 | `78700eef35b09c190e627dba17af54f92e9db2f22b777d01cf1ef78ec3aa8923` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/acfun/acfun/acfun.json) |
| surge | `surge/acfun/acfun/acfun.list` | 12 | 310 | `09a147ebdddfb1b37e5003e2246d0193395d05822439da172bcea2420671ec3c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/acfun/acfun/acfun.list) |

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