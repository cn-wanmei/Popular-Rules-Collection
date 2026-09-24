<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/material-symbols/service.svg" alt="Bank of Communications 图标" width="72" height="72">

# Bank of Communications — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `bocom` |
| 类型 | service |
| Provider / 服务集 | `bocom` |
| 规则浏览路径 | `bocom/bocom/bocom.yaml` |
| 语义规则数量 | **6** |
| 语义 SHA-256 | `3ca27d2fbeaef746a042a2830124ed6241fddb6df9769b5794a1d4e3439bb53f` |
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

所属服务集：[bocom](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/bocom/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/bocom/bocom/bocom.yaml` | 6 | 141 | `ae6af446f33218ae6d73dc91419606306f4f00a7dcca9df56dc4d4d005078607` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/bocom/bocom/bocom.yaml) |
| loon | `loon/bocom/bocom/bocom.list` | 6 | 170 | `19b922df23fab5a62116ab2102fcdb25fe4e064b7dd0f53beb07aba4fd4e3765` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/bocom/bocom/bocom.list) |
| mihomo | `mihomo/bocom/bocom/bocom.yaml` | 6 | 203 | `6c8eecfd1adf15a4ac3e8b706caa6afdfa0701b7af0700a75d2b6c6ef522b9cb` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/bocom/bocom/bocom.yaml) |
| quantumultx | `quantumultx/bocom/bocom/bocom.list` | 6 | 206 | `16223f0592a3ee11703e0c5c28b59f0f085e385b3e00d98be93cc23767295991` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/bocom/bocom/bocom.list) |
| shadowrocket | `shadowrocket/bocom/bocom/bocom.list` | 6 | 170 | `19b922df23fab5a62116ab2102fcdb25fe4e064b7dd0f53beb07aba4fd4e3765` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/bocom/bocom/bocom.list) |
| singbox | `singbox/bocom/bocom/bocom.json` | 0 | 233 | `3a961be2511efeea5dc33c88240dff3f16571c325fb51bd402ef773f211e26ed` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/bocom/bocom/bocom.json) |
| surge | `surge/bocom/bocom/bocom.list` | 6 | 170 | `19b922df23fab5a62116ab2102fcdb25fe4e064b7dd0f53beb07aba4fd4e3765` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/bocom/bocom/bocom.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/bocom/bocom/bocom.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/bocom/bocom/bocom.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/bocom/bocom/bocom.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/bocom/bocom/bocom.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/bocom/bocom/bocom.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/bocom/bocom/bocom.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/bocom/bocom/bocom.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  bocom:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/bocom/bocom/bocom.yaml"
    path: ./ruleset/bocom.yaml
    interval: 86400

rules:
  - RULE-SET,bocom,PROXY
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