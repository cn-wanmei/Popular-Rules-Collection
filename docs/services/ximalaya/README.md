<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/lucide/service.svg" alt="Ximalaya 图标" width="72" height="72">

# Ximalaya — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `ximalaya_aggregate` |
| 类型 | provider_aggregate |
| Provider / 服务集 | `ximalaya` |
| 规则浏览路径 | `ximalaya/ximalaya.yaml` |
| 语义规则数量 | **5** |
| 语义 SHA-256 | `c27fa6a6e13fc00118ae0e1a39537b8f35a7b24f4285d20a18dfab3f59aa0f5e` |
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

所属服务集：[ximalaya](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/ximalaya/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/ximalaya/ximalaya.yaml` | 5 | 136 | `1fab6ddbe73b126273077d22df36d76cb45e95434450ac8ece816648e11ec47e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/ximalaya/ximalaya.yaml) |
| loon | `loon/ximalaya/ximalaya.list` | 5 | 157 | `9ea6041a2fd02aabd775ecfa1b0401a91fe38e8bb5fa9d2ea38704be46a274a7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/ximalaya/ximalaya.list) |
| mihomo | `mihomo/ximalaya/ximalaya.yaml` | 5 | 186 | `a20256c79df26df67581308c9376a4e72ea0bbe5183fbd21ffa0f887f4b2f7d1` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/ximalaya/ximalaya.yaml) |
| quantumultx | `quantumultx/ximalaya/ximalaya.list` | 5 | 187 | `3a8cbc6fef199e6a0e2c580ef0149c8a6f1a0100238bdd891800607e77f47840` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/ximalaya/ximalaya.list) |
| shadowrocket | `shadowrocket/ximalaya/ximalaya.list` | 5 | 157 | `9ea6041a2fd02aabd775ecfa1b0401a91fe38e8bb5fa9d2ea38704be46a274a7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/ximalaya/ximalaya.list) |
| singbox | `singbox/ximalaya/ximalaya.json` | 0 | 223 | `417d6d7f27cc110b8491c35ad94a6934cd0806dce0d7dbbe5b48f54c6ea3307b` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/ximalaya/ximalaya.json) |
| surge | `surge/ximalaya/ximalaya.list` | 5 | 157 | `9ea6041a2fd02aabd775ecfa1b0401a91fe38e8bb5fa9d2ea38704be46a274a7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/ximalaya/ximalaya.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/ximalaya/ximalaya.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/ximalaya/ximalaya.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/ximalaya/ximalaya.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/ximalaya/ximalaya.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/ximalaya/ximalaya.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/ximalaya/ximalaya.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/ximalaya/ximalaya.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  ximalaya_aggregate:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/ximalaya/ximalaya.yaml"
    path: ./ruleset/ximalaya_aggregate.yaml
    interval: 86400

rules:
  - RULE-SET,ximalaya_aggregate,PROXY
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