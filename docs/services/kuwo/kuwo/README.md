<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/tabler/service.svg" alt="Kuwo 图标" width="72" height="72">

# Kuwo — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `kuwo` |
| 类型 | service |
| Provider / 服务集 | `kuwo` |
| 规则浏览路径 | `kuwo/kuwo/kuwo.yaml` |
| 语义规则数量 | **3** |
| 语义 SHA-256 | `56a09be2a42d3fd790d07df8d0a796499e6415f43d1c0d15a7f2dbc822a2c39b` |
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

所属服务集：[kuwo](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/kuwo/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/kuwo/kuwo/kuwo.yaml` | 3 | 64 | `084dff057272b7b7978b7b5f33868746d7b37c1205b52f841feb65fb8a0c1d36` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/kuwo/kuwo/kuwo.yaml) |
| loon | `loon/kuwo/kuwo/kuwo.list` | 3 | 69 | `b9e07a995b53848adcc1c780e51e5ec4245da8824ffcc9e423496d07d6b9a4f6` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/kuwo/kuwo/kuwo.list) |
| mihomo | `mihomo/kuwo/kuwo/kuwo.yaml` | 3 | 90 | `b7abf22a0a31e483de018078ffd61e84c34af2fe6ee2006ada34e799506c1ec8` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/kuwo/kuwo/kuwo.yaml) |
| quantumultx | `quantumultx/kuwo/kuwo/kuwo.list` | 3 | 87 | `7f41146105332b46d6028255a37caf0d3e817d892c6245633c3a36c284421564` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/kuwo/kuwo/kuwo.list) |
| shadowrocket | `shadowrocket/kuwo/kuwo/kuwo.list` | 3 | 69 | `b9e07a995b53848adcc1c780e51e5ec4245da8824ffcc9e423496d07d6b9a4f6` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/kuwo/kuwo/kuwo.list) |
| singbox | `singbox/kuwo/kuwo/kuwo.json` | 0 | 141 | `89ce757c160348f9414bddf6fc4029cbc2372efeae722c4ac876168966e1a797` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/kuwo/kuwo/kuwo.json) |
| surge | `surge/kuwo/kuwo/kuwo.list` | 3 | 69 | `b9e07a995b53848adcc1c780e51e5ec4245da8824ffcc9e423496d07d6b9a4f6` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/kuwo/kuwo/kuwo.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/kuwo/kuwo/kuwo.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/kuwo/kuwo/kuwo.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/kuwo/kuwo/kuwo.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/kuwo/kuwo/kuwo.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/kuwo/kuwo/kuwo.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/kuwo/kuwo/kuwo.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/kuwo/kuwo/kuwo.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  kuwo:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/kuwo/kuwo/kuwo.yaml"
    path: ./ruleset/kuwo.yaml
    interval: 86400

rules:
  - RULE-SET,kuwo,PROXY
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