<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/shopify.png" alt="Shopify 图标" width="72" height="72">

# Shopify — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `shopify` |
| 类型 | service |
| Provider / 服务集 | `shopify` |
| 规则浏览路径 | `shopify/shopify/shopify.yaml` |
| 语义规则数量 | **8** |
| 语义 SHA-256 | `78a2a22b2f64cff64c9f3b6565cfb4bd6b8169b9ef58549c74e681e29404a21b` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标：**Official / Brand Native**

- Identity：`brand.shopify`
- 来源：Current V3 已发布品牌身份资产
- Icon Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/shopify.png`
- Digest：`c49bdc344bf4a5a14a548314ce779a50f32c81d14af68129c7d9cce6ad52706f`

本服务存在可信品牌身份，因此 V4 不使用九风格 fallback 重绘该品牌 Logo。

风格层参考：Lucide / Tabler / Phosphor / Material Symbols / Fluent UI / Heroicons / Remix / Bootstrap / Solar。

## 3. 服务集与层级

所属服务集：[shopify](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/shopify/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/shopify/shopify/shopify.yaml` | 16 | 339 | `02b4fcf569eb0f78f927e2949a023bcd333c5d5a38b9da95dabdfb51c42de253` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/shopify/shopify/shopify.yaml) |
| loon | `loon/shopify/shopify/shopify.list` | 16 | 448 | `a6649d50d571b65a5be41d294f1bc0036f60f39b3cdd79f010376faeff2433bc` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/shopify/shopify/shopify.list) |
| mihomo | `mihomo/shopify/shopify/shopify.yaml` | 16 | 521 | `6fd1581fa9f1a9c2f5b7852c3e58834f130651e842475f44f2eb62be5501dadf` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/shopify/shopify/shopify.yaml) |
| quantumultx | `quantumultx/shopify/shopify/shopify.list` | 16 | 544 | `0724f2b7d8885102e46ab6a4597dac5738ab2d265c2dc4b70246da7f20d37248` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/shopify/shopify/shopify.list) |
| shadowrocket | `shadowrocket/shopify/shopify/shopify.list` | 16 | 448 | `a6649d50d571b65a5be41d294f1bc0036f60f39b3cdd79f010376faeff2433bc` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/shopify/shopify/shopify.list) |
| singbox | `singbox/shopify/shopify/shopify.json` | 0 | 481 | `89d2bfdb7e381bc2bd781d1a6de69127c636eb405d26a0306e0a5caecbddabff` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/shopify/shopify/shopify.json) |
| surge | `surge/shopify/shopify/shopify.list` | 16 | 448 | `a6649d50d571b65a5be41d294f1bc0036f60f39b3cdd79f010376faeff2433bc` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/shopify/shopify/shopify.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/shopify/shopify/shopify.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/shopify/shopify/shopify.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/shopify/shopify/shopify.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/shopify/shopify/shopify.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/shopify/shopify/shopify.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/shopify/shopify/shopify.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/shopify/shopify/shopify.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  shopify:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/shopify/shopify/shopify.yaml"
    path: ./ruleset/shopify.yaml
    interval: 86400

rules:
  - RULE-SET,shopify,PROXY
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