<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/lucide/service.svg" alt="Bahamut 图标" width="72" height="72">

# Bahamut — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `bahamut` |
| 类型 | service |
| Provider / 服务集 | `bahamut` |
| 规则浏览路径 | `bahamut/bahamut/bahamut.yaml` |
| 语义规则数量 | **7** |
| 语义 SHA-256 | `87c3a0dc32c8c700be43c78458b1290bff33d6dfcb4939f001373ba216084922` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标：**lucide semantic fallback**

- Style：`lucide`
- Identity：`semantic.fallback.lucide`
- 本地 V4 Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/lucide/service.svg`
- 语义：仅用于完整覆盖规则服务，不代表官方品牌 Logo。

风格层参考：Lucide / Tabler / Phosphor / Material Symbols / Fluent UI / Heroicons / Remix / Bootstrap / Solar。

## 3. 服务集与层级

所属服务集：[bahamut](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/bahamut/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/bahamut/bahamut/bahamut.yaml` | 7 | 167 | `41d0bc4db83afc92ba41e2ad85cc111491e6d7f1dfa4d8c93183997cc4b947d4` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/bahamut/bahamut/bahamut.yaml) |
| loon | `loon/bahamut/bahamut/bahamut.list` | 7 | 185 | `7db2e4f1a024b98375e6b9feab69cf9bea7ba81a2fbd33b9f9e3319759f97c44` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/bahamut/bahamut/bahamut.list) |
| mihomo | `mihomo/bahamut/bahamut/bahamut.yaml` | 7 | 222 | `c484754fa4f64fb5304feb739d44059ff16b945d860be32f164839a8e08a085c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/bahamut/bahamut/bahamut.yaml) |
| quantumultx | `quantumultx/bahamut/bahamut/bahamut.list` | 7 | 227 | `3d96c6585c75e312034d960133f5e81abb43ec6389e003e711527bc9f860c7a7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/bahamut/bahamut/bahamut.list) |
| shadowrocket | `shadowrocket/bahamut/bahamut/bahamut.list` | 7 | 185 | `7db2e4f1a024b98375e6b9feab69cf9bea7ba81a2fbd33b9f9e3319759f97c44` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/bahamut/bahamut/bahamut.list) |
| singbox | `singbox/bahamut/bahamut/bahamut.json` | 0 | 278 | `334c7a1df8c45e50b539f1ccd448ae0dc2927f0fdcb6fc2d2a0105fb4ef3f052` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/bahamut/bahamut/bahamut.json) |
| surge | `surge/bahamut/bahamut/bahamut.list` | 7 | 185 | `7db2e4f1a024b98375e6b9feab69cf9bea7ba81a2fbd33b9f9e3319759f97c44` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/bahamut/bahamut/bahamut.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/bahamut/bahamut/bahamut.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/bahamut/bahamut/bahamut.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/bahamut/bahamut/bahamut.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/bahamut/bahamut/bahamut.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/bahamut/bahamut/bahamut.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/bahamut/bahamut/bahamut.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/bahamut/bahamut/bahamut.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  bahamut:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/bahamut/bahamut/bahamut.yaml"
    path: ./ruleset/bahamut.yaml
    interval: 86400

rules:
  - RULE-SET,bahamut,PROXY
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