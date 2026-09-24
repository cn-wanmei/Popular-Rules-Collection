<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/tabler/service.svg" alt="Kuaishou 图标" width="72" height="72">

# Kuaishou — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `kuaishou_aggregate` |
| 类型 | provider_aggregate |
| Provider | `kuaishou` |
| 语义规则数量 | **678** |
| 语义 SHA-256 | `8cd109a51d33f0fc1105fc43f2ff371f2e36e6e9e91e0b1834b068b118ec60fb` |
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
| egern | `egern/kuaishou/kuaishou.yaml` | 678 | 13798 | `4b294e8c9760eecc5e71882bf774ba5d970dbba2566b3988aa571c78e8f05210` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/kuaishou/kuaishou.yaml) |
| loon | `loon/kuaishou/kuaishou.list` | 678 | 19203 | `9e69459ff1ea9978ccd99b73b11b613336a0313bd8412dd6e68ed9b574c8ee0f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/kuaishou/kuaishou.list) |
| mihomo | `mihomo/kuaishou/kuaishou.yaml` | 678 | 21924 | `7d1c030a3850a49d91f0293a5ee0346654d9ea0744b0722414fb7b630f503aa9` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/kuaishou/kuaishou.yaml) |
| quantumultx | `quantumultx/kuaishou/kuaishou.list` | 678 | 23271 | `ff2ef71e5c4c89ef3331d1661d3466c44ebbd1f1cc92c1da4994847c782ed396` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/kuaishou/kuaishou.list) |
| shadowrocket | `shadowrocket/kuaishou/kuaishou.list` | 678 | 19203 | `9e69459ff1ea9978ccd99b73b11b613336a0313bd8412dd6e68ed9b574c8ee0f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/kuaishou/kuaishou.list) |
| singbox | `singbox/kuaishou/kuaishou.json` | 0 | 17250 | `65c6bc65728448f6dacb99e1b741fb4fddaf1301d8fc526344d987127963007b` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/kuaishou/kuaishou.json) |
| surge | `surge/kuaishou/kuaishou.list` | 678 | 19203 | `9e69459ff1ea9978ccd99b73b11b613336a0313bd8412dd6e68ed9b574c8ee0f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/kuaishou/kuaishou.list) |

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