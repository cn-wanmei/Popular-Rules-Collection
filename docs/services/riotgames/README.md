<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/lucide/service.svg" alt="Riot Games 图标" width="72" height="72">

# Riot Games — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `riotgames_aggregate` |
| 类型 | provider_aggregate |
| Provider | `riotgames` |
| 语义规则数量 | **55** |
| 语义 SHA-256 | `c42786b34be14f0f775346284a2a5ee299b17f5b47435de2613439216a7aec2b` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**lucide semantic fallback**

- Style：`lucide`
- Identity：`semantic.fallback.lucide`
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/lucide/service.svg`
- 该图标用于覆盖缺失身份，不代表官方品牌 Logo。

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/riotgames/riotgames.yaml` | 55 | 1228 | `1cf2012e12278ac3b02e70a5eaf67b3ccd6868fbaa1658f4d725f49f19445b81` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/riotgames/riotgames.yaml) |
| loon | `loon/riotgames/riotgames.list` | 55 | 1649 | `fe4b0f5b884fe420737cb89399275dab0f021801768d11135324b1eda49c599b` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/riotgames/riotgames.list) |
| mihomo | `mihomo/riotgames/riotgames.yaml` | 55 | 1878 | `c385c1fc9d1f2904657198474ca967cd04f95fefc1185babfe6de3317d9ec428` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/riotgames/riotgames.yaml) |
| quantumultx | `quantumultx/riotgames/riotgames.list` | 55 | 1979 | `0c8d78e77965f6264068a2981f66cb25c6ab0886b39c404193c81c01d198bfb7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/riotgames/riotgames.list) |
| shadowrocket | `shadowrocket/riotgames/riotgames.list` | 55 | 1649 | `fe4b0f5b884fe420737cb89399275dab0f021801768d11135324b1eda49c599b` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/riotgames/riotgames.list) |
| singbox | `singbox/riotgames/riotgames.json` | 0 | 1565 | `38c930af0b85cda71aaf777b8391e9061bf2428c61844ea18be74152751821b8` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/riotgames/riotgames.json) |
| surge | `surge/riotgames/riotgames.list` | 55 | 1649 | `fe4b0f5b884fe420737cb89399275dab0f021801768d11135324b1eda49c599b` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/riotgames/riotgames.list) |

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