<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/material-symbols/service.svg" alt="PPTV 图标" width="72" height="72">

# PPTV — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `pptv_aggregate` |
| 类型 | provider_aggregate |
| Provider / 服务集 | `pptv` |
| 规则浏览路径 | `pptv/pptv.yaml` |
| 语义规则数量 | **19** |
| 语义 SHA-256 | `19cdaa4beceaa5ab066426c0c6fd2d431018871d99f37fb3d2bae2d4b942ec50` |
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

所属服务集：[pptv](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/pptv/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/pptv/pptv.yaml` | 19 | 342 | `8d46aae74e97de441e56061b7362d29ecea331fc58b5f4b52a6726f7cdfd784d` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/pptv/pptv.yaml) |
| loon | `loon/pptv/pptv.list` | 19 | 475 | `29e820ad7185ab76bf3454efaadc774e12df1fe9c6bc0878da09ed62d47dcee1` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/pptv/pptv.list) |
| mihomo | `mihomo/pptv/pptv.yaml` | 19 | 560 | `eeeff7ae42695ea9168f5fed690e0a94a57649a41a4e4005fb495e3667b332ce` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/pptv/pptv.yaml) |
| quantumultx | `quantumultx/pptv/pptv.list` | 19 | 589 | `4cd41a552e2e58a19f1bcc940012a151ae1be7fed4c326203aaf3791081ef02d` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/pptv/pptv.list) |
| shadowrocket | `shadowrocket/pptv/pptv.list` | 19 | 475 | `29e820ad7185ab76bf3454efaadc774e12df1fe9c6bc0878da09ed62d47dcee1` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/pptv/pptv.list) |
| singbox | `singbox/pptv/pptv.json` | 0 | 499 | `4b6de1b8cb020ae53146718bfc70307213607a0d0ac1f385319cf6fa94739c75` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/pptv/pptv.json) |
| surge | `surge/pptv/pptv.list` | 19 | 475 | `29e820ad7185ab76bf3454efaadc774e12df1fe9c6bc0878da09ed62d47dcee1` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/pptv/pptv.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/pptv/pptv.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/pptv/pptv.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/pptv/pptv.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/pptv/pptv.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/pptv/pptv.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/pptv/pptv.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/pptv/pptv.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  pptv_aggregate:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/pptv/pptv.yaml"
    path: ./ruleset/pptv_aggregate.yaml
    interval: 86400

rules:
  - RULE-SET,pptv_aggregate,PROXY
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