<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/heroicons/service.svg" alt="China Mobile 图标" width="72" height="72">

# China Mobile — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `chinamobile_aggregate` |
| 类型 | provider_aggregate |
| Provider / 服务集 | `chinamobile` |
| 规则浏览路径 | `chinamobile/chinamobile.yaml` |
| 语义规则数量 | **38** |
| 语义 SHA-256 | `5b3b653d7ed6e63afa1653d581c38e98729d3f4956a53ec9021a449537c021c5` |
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

所属服务集：[chinamobile](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/chinamobile/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/chinamobile/chinamobile.yaml` | 38 | 735 | `98e591e707046ba63ef1ae361ad34f44df5a165f16f8f92392d3e05dc39af893` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/chinamobile/chinamobile.yaml) |
| loon | `loon/chinamobile/chinamobile.list` | 38 | 1001 | `be232aacdb8d1cb70d0264e1d91c6e0de5d5c78a8d906aa5710fc79d2f546733` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/chinamobile/chinamobile.list) |
| mihomo | `mihomo/chinamobile/chinamobile.yaml` | 38 | 1162 | `d7c8f536c574c620ca031a875d51b560b0b5e8ad2b5bb4ffd5ff4c53e91ac4b0` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/chinamobile/chinamobile.yaml) |
| quantumultx | `quantumultx/chinamobile/chinamobile.list` | 38 | 1231 | `22f41d3c67342ab635e927bdd8787cb957952901c54bd581a72a7c0d6c67e360` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/chinamobile/chinamobile.list) |
| shadowrocket | `shadowrocket/chinamobile/chinamobile.list` | 38 | 1001 | `be232aacdb8d1cb70d0264e1d91c6e0de5d5c78a8d906aa5710fc79d2f546733` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/chinamobile/chinamobile.list) |
| singbox | `singbox/chinamobile/chinamobile.json` | 0 | 1001 | `7a9606eee6d4d9981b95e4e1e548942aa2d2b69e484972e503121f2460df368f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/chinamobile/chinamobile.json) |
| surge | `surge/chinamobile/chinamobile.list` | 38 | 1001 | `be232aacdb8d1cb70d0264e1d91c6e0de5d5c78a8d906aa5710fc79d2f546733` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/chinamobile/chinamobile.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/chinamobile/chinamobile.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/chinamobile/chinamobile.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/chinamobile/chinamobile.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/chinamobile/chinamobile.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/chinamobile/chinamobile.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/chinamobile/chinamobile.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/chinamobile/chinamobile.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  chinamobile_aggregate:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/chinamobile/chinamobile.yaml"
    path: ./ruleset/chinamobile_aggregate.yaml
    interval: 86400

rules:
  - RULE-SET,chinamobile_aggregate,PROXY
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