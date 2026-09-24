<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/tabler/service.svg" alt="UnionPay 图标" width="72" height="72">

# UnionPay — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `unionpay` |
| 类型 | service |
| Provider / 服务集 | `unionpay` |
| 规则浏览路径 | `unionpay/unionpay/unionpay.yaml` |
| 语义规则数量 | **16** |
| 语义 SHA-256 | `3cbbe321186965e7ea04b56fbea849aa72fd27db627a38c8689e27cb78b5edf0` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标：**tabler semantic fallback**

- Style：`tabler`
- Identity：`semantic.fallback.tabler`
- 本地 V4 Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/tabler/service.svg`
- 语义：仅用于完整覆盖规则服务，不代表官方品牌 Logo。

风格层参考：Lucide / Tabler / Phosphor / Material Symbols / Fluent UI / Heroicons / Remix / Bootstrap / Solar。

## 3. 服务集与层级

所属服务集：[unionpay](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/unionpay/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/unionpay/unionpay/unionpay.yaml` | 16 | 348 | `b2a646c14bc080f27cb2b534598cfa0a07235a77d724c10a1daf3388497341aa` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/unionpay/unionpay/unionpay.yaml) |
| loon | `loon/unionpay/unionpay/unionpay.list` | 16 | 457 | `0debe3092e2e14067698e9a90bc7fc143a255d41c01d886121ddba067003831f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/unionpay/unionpay/unionpay.list) |
| mihomo | `mihomo/unionpay/unionpay/unionpay.yaml` | 16 | 530 | `9ca101fee251cb8068d98e5bf92654c734914863350c496acc857293cd4068ac` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/unionpay/unionpay/unionpay.yaml) |
| quantumultx | `quantumultx/unionpay/unionpay/unionpay.list` | 16 | 553 | `03efad8a159c36fd79cc579b1fd53d86390444403993bb631b9cff90d0631b58` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/unionpay/unionpay/unionpay.list) |
| shadowrocket | `shadowrocket/unionpay/unionpay/unionpay.list` | 16 | 457 | `0debe3092e2e14067698e9a90bc7fc143a255d41c01d886121ddba067003831f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/unionpay/unionpay/unionpay.list) |
| singbox | `singbox/unionpay/unionpay/unionpay.json` | 0 | 490 | `9130395bb7f5b939a81b00c7e400986bda7c94f2af0d9d2bfae866c7ce2d60ef` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/unionpay/unionpay/unionpay.json) |
| surge | `surge/unionpay/unionpay/unionpay.list` | 16 | 457 | `0debe3092e2e14067698e9a90bc7fc143a255d41c01d886121ddba067003831f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/unionpay/unionpay/unionpay.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/unionpay/unionpay/unionpay.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/unionpay/unionpay/unionpay.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/unionpay/unionpay/unionpay.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/unionpay/unionpay/unionpay.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/unionpay/unionpay/unionpay.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/unionpay/unionpay/unionpay.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/unionpay/unionpay/unionpay.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  unionpay:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/unionpay/unionpay/unionpay.yaml"
    path: ./ruleset/unionpay.yaml
    interval: 86400

rules:
  - RULE-SET,unionpay,PROXY
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