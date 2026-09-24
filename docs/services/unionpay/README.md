<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/solar/service.svg" alt="UnionPay 图标" width="72" height="72">

# UnionPay — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `unionpay_aggregate` |
| 类型 | provider_aggregate |
| Provider / 服务集 | `unionpay` |
| 规则浏览路径 | `unionpay/unionpay.yaml` |
| 语义规则数量 | **16** |
| 语义 SHA-256 | `bedf21282bc5b36aaa05f5afedaef215b37fda0d09ea365f3d1092941a8a4980` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标：**solar semantic fallback**

- Style：`solar`
- Identity：`semantic.fallback.solar`
- 本地 V4 Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/solar/service.svg`
- 语义：仅用于完整覆盖规则服务，不代表官方品牌 Logo。

风格层参考：Lucide / Tabler / Phosphor / Material Symbols / Fluent UI / Heroicons / Remix / Bootstrap / Solar。

## 3. 服务集与层级

所属服务集：[unionpay](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/unionpay/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/unionpay/unionpay.yaml` | 16 | 348 | `f1db919c1aeec42f25644be1857c0dfd2ac9ff4858cf3f7808a2ccd68b154416` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/unionpay/unionpay.yaml) |
| loon | `loon/unionpay/unionpay.list` | 16 | 457 | `2f473dc96dd219ba9067aca4ab056c429fde5ed9272a7f5bcdd4286574724b9a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/unionpay/unionpay.list) |
| mihomo | `mihomo/unionpay/unionpay.yaml` | 16 | 530 | `7dcb65ae30eabeb95263789ddc7173bbeda63b4be58078f29e5299892144d0fd` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/unionpay/unionpay.yaml) |
| quantumultx | `quantumultx/unionpay/unionpay.list` | 16 | 553 | `2b97493228a3d8cd5bfd56a28ff96889b3cf1133a7417d30b6ec1a133ee9c4c1` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/unionpay/unionpay.list) |
| shadowrocket | `shadowrocket/unionpay/unionpay.list` | 16 | 457 | `2f473dc96dd219ba9067aca4ab056c429fde5ed9272a7f5bcdd4286574724b9a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/unionpay/unionpay.list) |
| singbox | `singbox/unionpay/unionpay.json` | 0 | 490 | `6b2ca7027be7c0adc42c421cc5ec10f6e85cb73a543d2946d40f5ad573e1796c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/unionpay/unionpay.json) |
| surge | `surge/unionpay/unionpay.list` | 16 | 457 | `2f473dc96dd219ba9067aca4ab056c429fde5ed9272a7f5bcdd4286574724b9a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/unionpay/unionpay.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/unionpay/unionpay.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/unionpay/unionpay.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/unionpay/unionpay.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/unionpay/unionpay.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/unionpay/unionpay.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/unionpay/unionpay.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/unionpay/unionpay.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  unionpay_aggregate:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/unionpay/unionpay.yaml"
    path: ./ruleset/unionpay_aggregate.yaml
    interval: 86400

rules:
  - RULE-SET,unionpay_aggregate,PROXY
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