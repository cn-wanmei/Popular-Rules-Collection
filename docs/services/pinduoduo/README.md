<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/material-symbols/service.svg" alt="Pinduoduo 图标" width="72" height="72">

# Pinduoduo — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `pinduoduo_aggregate` |
| 类型 | provider_aggregate |
| Provider / 服务集 | `pinduoduo` |
| 规则浏览路径 | `pinduoduo/pinduoduo.yaml` |
| 语义规则数量 | **3** |
| 语义 SHA-256 | `8ffa3dd356f2e65ea47a102f058cbd43b5d2e56ef0872c2e01cac3e43d285f95` |
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

所属服务集：[pinduoduo](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/pinduoduo/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/pinduoduo/pinduoduo.yaml` | 3 | 76 | `6d7589dc9a0cd94064c0d0290da584838c1806b92f35f69be5818be7cd664106` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/pinduoduo/pinduoduo.yaml) |
| loon | `loon/pinduoduo/pinduoduo.list` | 3 | 81 | `5c72d6b5f95cb88c69ce2276d709310f46700a565f03b4a05485a1e1e9810fec` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/pinduoduo/pinduoduo.list) |
| mihomo | `mihomo/pinduoduo/pinduoduo.yaml` | 3 | 102 | `fcb2c2acd00029a7f875b6a4d5d8baa64f64ee20166c14926a76297362280f14` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/pinduoduo/pinduoduo.yaml) |
| quantumultx | `quantumultx/pinduoduo/pinduoduo.list` | 3 | 99 | `860e7c1a932074a6d0b7cf8c3fb4319ccc2fbb3ab3f06a21038c6e5112598267` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/pinduoduo/pinduoduo.list) |
| shadowrocket | `shadowrocket/pinduoduo/pinduoduo.list` | 3 | 81 | `5c72d6b5f95cb88c69ce2276d709310f46700a565f03b4a05485a1e1e9810fec` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/pinduoduo/pinduoduo.list) |
| singbox | `singbox/pinduoduo/pinduoduo.json` | 0 | 153 | `dcaf78dc6d8642c3fcb55b145e733713055f07f7fc3e22ff237da362b639af53` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/pinduoduo/pinduoduo.json) |
| surge | `surge/pinduoduo/pinduoduo.list` | 3 | 81 | `5c72d6b5f95cb88c69ce2276d709310f46700a565f03b4a05485a1e1e9810fec` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/pinduoduo/pinduoduo.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/pinduoduo/pinduoduo.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/pinduoduo/pinduoduo.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/pinduoduo/pinduoduo.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/pinduoduo/pinduoduo.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/pinduoduo/pinduoduo.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/pinduoduo/pinduoduo.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/pinduoduo/pinduoduo.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  pinduoduo_aggregate:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/pinduoduo/pinduoduo.yaml"
    path: ./ruleset/pinduoduo_aggregate.yaml
    interval: 86400

rules:
  - RULE-SET,pinduoduo_aggregate,PROXY
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