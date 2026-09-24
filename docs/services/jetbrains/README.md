<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/jetbrains.png" alt="JetBrains 图标" width="72" height="72">

# JetBrains — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `jetbrains_aggregate` |
| 类型 | provider_aggregate |
| Provider / 服务集 | `jetbrains` |
| 规则浏览路径 | `jetbrains/jetbrains.yaml` |
| 语义规则数量 | **25** |
| 语义 SHA-256 | `fe6be2518ee347f1ae32eef31dccbd99d645c55a141414e2e4c814a042c6662b` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标：**Official / Brand Native**

- Identity：`brand.jetbrains`
- 来源：Current V3 已发布品牌身份资产
- Icon Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/jetbrains.png`
- Digest：`a4177164adb32fabd7fb361c998d141d7f0c05ca91c7286849d662e582c4bc11`

本服务存在可信品牌身份，因此 V4 不使用九风格 fallback 重绘该品牌 Logo。

风格层参考：Lucide / Tabler / Phosphor / Material Symbols / Fluent UI / Heroicons / Remix / Bootstrap / Solar。

## 3. 服务集与层级

所属服务集：[jetbrains](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/jetbrains/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/jetbrains/jetbrains.yaml` | 25 | 508 | `86d0293e2edc38abc818333ec50038c440abf6916b07a8944778092c9f607e7e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/jetbrains/jetbrains.yaml) |
| loon | `loon/jetbrains/jetbrains.list` | 25 | 689 | `48f53f799b186f18d8cc28d60830c07ab369db05776ec00706b6d732076dd8bb` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/jetbrains/jetbrains.list) |
| mihomo | `mihomo/jetbrains/jetbrains.yaml` | 25 | 798 | `18a7646f1a52a9075da31bb98b3dbf4111cf5afb7cce44a54d23a6f6df4285c4` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/jetbrains/jetbrains.yaml) |
| quantumultx | `quantumultx/jetbrains/jetbrains.list` | 25 | 839 | `bba3f0bab49cad1ea8f1257e05a01079c571d6b13d55ff6fdee7bcf8696e7871` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/jetbrains/jetbrains.list) |
| shadowrocket | `shadowrocket/jetbrains/jetbrains.list` | 25 | 689 | `48f53f799b186f18d8cc28d60830c07ab369db05776ec00706b6d732076dd8bb` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/jetbrains/jetbrains.list) |
| singbox | `singbox/jetbrains/jetbrains.json` | 0 | 695 | `a8ced873ec06bda6d99bf296ed82cd713e29a813e0b58616d9e7cf864bf679d4` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/jetbrains/jetbrains.json) |
| surge | `surge/jetbrains/jetbrains.list` | 25 | 689 | `48f53f799b186f18d8cc28d60830c07ab369db05776ec00706b6d732076dd8bb` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/jetbrains/jetbrains.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/jetbrains/jetbrains.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/jetbrains/jetbrains.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/jetbrains/jetbrains.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/jetbrains/jetbrains.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/jetbrains/jetbrains.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/jetbrains/jetbrains.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/jetbrains/jetbrains.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  jetbrains_aggregate:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/jetbrains/jetbrains.yaml"
    path: ./ruleset/jetbrains_aggregate.yaml
    interval: 86400

rules:
  - RULE-SET,jetbrains_aggregate,PROXY
```

## 6. 服务集与独立子服务

**服务集：** 适合较宽覆盖面。

**独立服务 / 子服务：** 适合精确分流；直接使用该服务自己的 Raw，不要从聚合规则手工拆分。

**父子规则同时加载：** 实际优先级由客户端规则顺序决定。

## 7. 更新、统计与完整性

| 检查项 | 权威来源 |
|---|---|
| 语义规则数量 / Service SHA-256 | `rule/_index.yaml` |
| 客户端文件 / rule_count / size / SHA-256 | `generated/manifest.json` |
| 当前 Icon 主层 / fallback | `assets/icons/v4/service-index.json` |
| Icon Release | `assets/icons/v4/release-pointer.json` |

统计口径：`rule_count` 是 Manifest 对客户端文件记录的字段，不同客户端可能有不同口径；服务本身的主要规则数量以 `rule/_index.yaml` 语义 `rule_count` 为准。

当前 Collection Date：`2026-09-24`；Release Generated At：`2026-09-24T04:39:15.367236+00:00`。

## 8. 相关入口

- [服务总目录](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/SERVICE_CATALOG.md)
- [V4 图标库](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/assets/icons/v4/README.md)
- [V4 Style Guide](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/ICON_STYLE_GUIDE_V4.md)
- [完整规则使用说明](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/RULE_USAGE_GUIDE.md)
- [规则索引](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/rule/_index.yaml)

[回到顶部](#top)