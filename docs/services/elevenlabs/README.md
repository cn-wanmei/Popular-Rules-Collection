<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/phosphor/service.svg" alt="ElevenLabs 图标" width="72" height="72">

# ElevenLabs — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `elevenlabs_aggregate` |
| 类型 | provider_aggregate |
| Provider / 服务集 | `elevenlabs` |
| 规则浏览路径 | `elevenlabs/elevenlabs.yaml` |
| 语义规则数量 | **2** |
| 语义 SHA-256 | `1b6866748729d5fc1d78e2bc4908658775c43dc348a0d885b6636113943449b4` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标：**phosphor semantic fallback**

- Style：`phosphor`
- Identity：`semantic.fallback.phosphor`
- 本地 V4 Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/phosphor/service.svg`
- 语义：仅用于完整覆盖规则服务，不代表官方品牌 Logo。

风格层参考：Lucide / Tabler / Phosphor / Material Symbols / Fluent UI / Heroicons / Remix / Bootstrap / Solar。

## 3. 服务集与层级

所属服务集：[elevenlabs](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/elevenlabs/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/elevenlabs/elevenlabs.yaml` | 2 | 60 | `0afe7641b892b88413405c44d8b8b03f663cefe10d1ddd0d2071ab7deac8d192` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/elevenlabs/elevenlabs.yaml) |
| loon | `loon/elevenlabs/elevenlabs.list` | 2 | 57 | `42763bec3b93eadfd570a08593476302a2ae1a57aad578eff566a4b4a479950e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/elevenlabs/elevenlabs.list) |
| mihomo | `mihomo/elevenlabs/elevenlabs.yaml` | 2 | 74 | `62c5c3aeb9a088b64854c4eab09565a38f69135e4dbdee3541fc79f6f558b0af` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/elevenlabs/elevenlabs.yaml) |
| quantumultx | `quantumultx/elevenlabs/elevenlabs.list` | 2 | 69 | `0153cbaace43dd3a133969144acfed29591e04503e2a09105df09dd6966c3c86` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/elevenlabs/elevenlabs.list) |
| shadowrocket | `shadowrocket/elevenlabs/elevenlabs.list` | 2 | 57 | `42763bec3b93eadfd570a08593476302a2ae1a57aad578eff566a4b4a479950e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/elevenlabs/elevenlabs.list) |
| singbox | `singbox/elevenlabs/elevenlabs.json` | 0 | 132 | `5dad1e10662ab1b565d113bf68fefb8bbc6a67b00685d7989b0500684365767a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/elevenlabs/elevenlabs.json) |
| surge | `surge/elevenlabs/elevenlabs.list` | 2 | 57 | `42763bec3b93eadfd570a08593476302a2ae1a57aad578eff566a4b4a479950e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/elevenlabs/elevenlabs.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/elevenlabs/elevenlabs.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/elevenlabs/elevenlabs.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/elevenlabs/elevenlabs.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/elevenlabs/elevenlabs.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/elevenlabs/elevenlabs.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/elevenlabs/elevenlabs.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/elevenlabs/elevenlabs.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  elevenlabs_aggregate:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/elevenlabs/elevenlabs.yaml"
    path: ./ruleset/elevenlabs_aggregate.yaml
    interval: 86400

rules:
  - RULE-SET,elevenlabs_aggregate,PROXY
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