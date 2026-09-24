<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/material-symbols/service.svg" alt="Blizzard Entertainment 图标" width="72" height="72">

# Blizzard Entertainment — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `blizzard_aggregate` |
| 类型 | provider_aggregate |
| Provider / 服务集 | `blizzard` |
| 规则浏览路径 | `blizzard/blizzard.yaml` |
| 语义规则数量 | **62** |
| 语义 SHA-256 | `f008dd3e5d8586d3a4a8edb04dda7deb528b188cd9b42c6f4e8a222e19a2a2e8` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标：**material-symbols semantic fallback**

- Style：`material-symbols`
- Identity：`semantic.fallback.material-symbols`
- 本地 V4 Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/material-symbols/service.svg`
- 语义：仅用于完整覆盖规则服务，不代表官方品牌 Logo。

风格层参考：Lucide / Tabler / Phosphor / Material Symbols / Fluent UI / Heroicons / Remix / Bootstrap / Solar。

## 3. 服务集与层级

所属服务集：[blizzard](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/blizzard/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/blizzard/blizzard.yaml` | 62 | 1552 | `860988e9b6c78bf4d0806959e08935792374c805af6ed0dda16a165ce8caaf7c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/blizzard/blizzard.yaml) |
| loon | `loon/blizzard/blizzard.list` | 62 | 1878 | `6ddd4778f0728ef5261b4609b5fbe3fb17c2cfedc4097f3003832063391fe80f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/blizzard/blizzard.list) |
| mihomo | `mihomo/blizzard/blizzard.yaml` | 62 | 2135 | `3f639462b312e2e3ce614d7167309067b5da4d2a89d8206fbfeb9e2e4da0123a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/blizzard/blizzard.yaml) |
| quantumultx | `quantumultx/blizzard/blizzard.list` | 62 | 2296 | `e3464331c99c31846f69ee1097ad5f134a5faa00afcbe53d316638f5fe3c34ed` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/blizzard/blizzard.list) |
| shadowrocket | `shadowrocket/blizzard/blizzard.list` | 62 | 1878 | `6ddd4778f0728ef5261b4609b5fbe3fb17c2cfedc4097f3003832063391fe80f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/blizzard/blizzard.list) |
| singbox | `singbox/blizzard/blizzard.json` | 0 | 1938 | `f25090a8dab624372445ccf5b1040c14b3fbc6cb772fa7df203d8a868f6644a1` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/blizzard/blizzard.json) |
| surge | `surge/blizzard/blizzard.list` | 62 | 1878 | `6ddd4778f0728ef5261b4609b5fbe3fb17c2cfedc4097f3003832063391fe80f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/blizzard/blizzard.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/blizzard/blizzard.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/blizzard/blizzard.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/blizzard/blizzard.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/blizzard/blizzard.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/blizzard/blizzard.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/blizzard/blizzard.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/blizzard/blizzard.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  blizzard_aggregate:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/blizzard/blizzard.yaml"
    path: ./ruleset/blizzard_aggregate.yaml
    interval: 86400

rules:
  - RULE-SET,blizzard_aggregate,PROXY
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