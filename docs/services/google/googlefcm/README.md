<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/heroicons/service.svg" alt="Google FCM 图标" width="72" height="72">

# Google FCM — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `googlefcm` |
| 类型 | service |
| Provider | `google` |
| 语义规则数量 | **13** |
| 语义 SHA-256 | `1e3d116a03f64650b9cc4b7803cf5c565e642003df11518f8fadf27a7255a0b4` |
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
| egern | `egern/google/googlefcm/googlefcm.yaml` | 13 | 378 | `7d9ce3304df0ddcead7d1500cecc736d711ff0436e7bbf42805e2eafb0ab83a4` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/google/googlefcm/googlefcm.yaml) |
| loon | `loon/google/googlefcm/googlefcm.list` | 13 | 463 | `d5416f51714c2a6e111c090136eaf04f90a352fdb549125dfefd63fa89259c85` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/google/googlefcm/googlefcm.list) |
| mihomo | `mihomo/google/googlefcm/googlefcm.yaml` | 13 | 524 | `f4adc194c1a8fd435cedecc165ad44745e869c22b5413233c46cb6db44fd2bbc` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/google/googlefcm/googlefcm.yaml) |
| quantumultx | `quantumultx/google/googlefcm/googlefcm.list` | 13 | 541 | `ce563c7fdabf600c1031bfcbecd471a4fe9eb0ccf8b8cfe6ca91f0da49ec4a2c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/google/googlefcm/googlefcm.list) |
| shadowrocket | `shadowrocket/google/googlefcm/googlefcm.list` | 13 | 463 | `d5416f51714c2a6e111c090136eaf04f90a352fdb549125dfefd63fa89259c85` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/google/googlefcm/googlefcm.list) |
| singbox | `singbox/google/googlefcm/googlefcm.json` | 0 | 505 | `44b2ab01b2f1e2b5b9d2870fdcbd74a950b3846910fc1b5198f13f384d953422` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/google/googlefcm/googlefcm.json) |
| surge | `surge/google/googlefcm/googlefcm.list` | 13 | 463 | `d5416f51714c2a6e111c090136eaf04f90a352fdb549125dfefd63fa89259c85` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/google/googlefcm/googlefcm.list) |

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