<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/heroicons/service.svg" alt="Prime Video 图标" width="72" height="72">

# Prime Video — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `primevideo` |
| 类型 | service |
| Provider / 服务集 | `amazon` |
| 规则浏览路径 | `amazon/primevideo/primevideo.yaml` |
| 语义规则数量 | **26** |
| 语义 SHA-256 | `2778598d3839159f9e2f1a0f1b13867e985e3aca7f06cce40a0ff1cabe2f7c7d` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标：**heroicons semantic fallback**

- Style：`heroicons`
- Identity：`semantic.fallback.heroicons`
- 本地 V4 Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/heroicons/service.svg`
- 语义：仅用于完整覆盖规则服务，不代表官方品牌 Logo。

风格层参考：Lucide / Tabler / Phosphor / Material Symbols / Fluent UI / Heroicons / Remix / Bootstrap / Solar。

## 3. 服务集与层级

所属服务集：[amazon](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/amazon/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/amazon/primevideo/primevideo.yaml` | 25 | 677 | `1a0f43b21bca7fb01632a416806f1ee79661f4fefbf67b15f32451d4632bc568` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/amazon/primevideo/primevideo.yaml) |
| loon | `loon/amazon/primevideo/primevideo.list` | 25 | 792 | `1dc4d514a0fe48105efffe3de5a2468372d391b71db16b687392b270aab27439` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/amazon/primevideo/primevideo.list) |
| mihomo | `mihomo/amazon/primevideo/primevideo.yaml` | 25 | 901 | `e6102e4b6aabd2028945fb7b413d033982b960b07858f0405b0389c592d8477e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/amazon/primevideo/primevideo.yaml) |
| quantumultx | `quantumultx/amazon/primevideo/primevideo.list` | 25 | 942 | `77b1e6b80f17b01813b3d169a6e62942bcab3eb3753f85032b0cb2b112a23620` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/amazon/primevideo/primevideo.list) |
| shadowrocket | `shadowrocket/amazon/primevideo/primevideo.list` | 25 | 792 | `1dc4d514a0fe48105efffe3de5a2468372d391b71db16b687392b270aab27439` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/amazon/primevideo/primevideo.list) |
| singbox | `singbox/amazon/primevideo/primevideo.json` | 0 | 892 | `e41d6423d25b49f626eade660b94d5f73c29b7f8b4cc575372116945eb1cd9ba` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/amazon/primevideo/primevideo.json) |
| surge | `surge/amazon/primevideo/primevideo.list` | 25 | 792 | `1dc4d514a0fe48105efffe3de5a2468372d391b71db16b687392b270aab27439` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/amazon/primevideo/primevideo.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/amazon/primevideo/primevideo.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/amazon/primevideo/primevideo.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/amazon/primevideo/primevideo.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/amazon/primevideo/primevideo.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/amazon/primevideo/primevideo.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/amazon/primevideo/primevideo.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/amazon/primevideo/primevideo.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  primevideo:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/amazon/primevideo/primevideo.yaml"
    path: ./ruleset/primevideo.yaml
    interval: 86400

rules:
  - RULE-SET,primevideo,PROXY
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