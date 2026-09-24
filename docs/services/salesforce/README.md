<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/phosphor/service.svg" alt="Salesforce 图标" width="72" height="72">

# Salesforce — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `salesforce_aggregate` |
| 类型 | provider_aggregate |
| Provider / 服务集 | `salesforce` |
| 规则浏览路径 | `salesforce/salesforce.yaml` |
| 语义规则数量 | **23** |
| 语义 SHA-256 | `5de6c7ab2d951420e2bfa60782f55ae620ae0019eaf75cf4008af50c67a4bd56` |
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

所属服务集：[salesforce](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/salesforce/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/salesforce/salesforce.yaml` | 23 | 469 | `03de0a3b234f0ed392945b2bee170502060bca4f77e0d39a37b1a98157f1ecf2` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/salesforce/salesforce.yaml) |
| loon | `loon/salesforce/salesforce.list` | 23 | 634 | `6e9a20d17a38d0e63e9ede0c482d4f459356ce03fdc53863496b13471c8a9a02` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/salesforce/salesforce.list) |
| mihomo | `mihomo/salesforce/salesforce.yaml` | 23 | 735 | `8bc0a2f598272f89ec7620efac6eeb3aa797ff1d63924463965f238d319b24a5` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/salesforce/salesforce.yaml) |
| quantumultx | `quantumultx/salesforce/salesforce.list` | 23 | 772 | `d900a1cf7b22e9d780c8900ab74f4ddfe9ad1e7dbe0ca3542b5479252254cb2b` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/salesforce/salesforce.list) |
| shadowrocket | `shadowrocket/salesforce/salesforce.list` | 23 | 634 | `6e9a20d17a38d0e63e9ede0c482d4f459356ce03fdc53863496b13471c8a9a02` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/salesforce/salesforce.list) |
| singbox | `singbox/salesforce/salesforce.json` | 0 | 646 | `0a8d8cec804dd6b0f5d3171dad64645e07149c3715727fa42730ed56bd27861b` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/salesforce/salesforce.json) |
| surge | `surge/salesforce/salesforce.list` | 23 | 634 | `6e9a20d17a38d0e63e9ede0c482d4f459356ce03fdc53863496b13471c8a9a02` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/salesforce/salesforce.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/salesforce/salesforce.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/salesforce/salesforce.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/salesforce/salesforce.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/salesforce/salesforce.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/salesforce/salesforce.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/salesforce/salesforce.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/salesforce/salesforce.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  salesforce_aggregate:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/salesforce/salesforce.yaml"
    path: ./ruleset/salesforce_aggregate.yaml
    interval: 86400

rules:
  - RULE-SET,salesforce_aggregate,PROXY
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