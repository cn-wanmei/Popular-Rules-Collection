<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/solar/service.svg" alt="Ximalaya 图标" width="72" height="72">

# Ximalaya — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `ximalaya` |
| 类型 | service |
| Provider / 服务集 | `ximalaya` |
| 规则浏览路径 | `ximalaya/ximalaya/ximalaya.yaml` |
| 语义规则数量 | **5** |
| 语义 SHA-256 | `ec97d96d52d63b9d95918333069cdce089de5f2c03267537e9d1757f58b7daaf` |
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

所属服务集：[ximalaya](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/ximalaya/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/ximalaya/ximalaya/ximalaya.yaml` | 5 | 136 | `549a52961092ffcf95f6cb33ff397e227dae477e2f07af3fdfcc6993011f8fdd` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/ximalaya/ximalaya/ximalaya.yaml) |
| loon | `loon/ximalaya/ximalaya/ximalaya.list` | 5 | 157 | `f720fcca26e01aab3d1e52e6e616fc9ebddca01b9d6744d25e3e762665860ae7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/ximalaya/ximalaya/ximalaya.list) |
| mihomo | `mihomo/ximalaya/ximalaya/ximalaya.yaml` | 5 | 186 | `dc42161c1065fd216d4bffd13ae9a6e5dd06ced67c42f6272c30840d48ade5d7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/ximalaya/ximalaya/ximalaya.yaml) |
| quantumultx | `quantumultx/ximalaya/ximalaya/ximalaya.list` | 5 | 187 | `5c8cf0ae9cb97877afd97da83e74529051a07a05297cac28924ab470fe72bf8a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/ximalaya/ximalaya/ximalaya.list) |
| shadowrocket | `shadowrocket/ximalaya/ximalaya/ximalaya.list` | 5 | 157 | `f720fcca26e01aab3d1e52e6e616fc9ebddca01b9d6744d25e3e762665860ae7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/ximalaya/ximalaya/ximalaya.list) |
| singbox | `singbox/ximalaya/ximalaya/ximalaya.json` | 0 | 223 | `8cd04eca54156fcf7d3a0f3bee921b9f994336c667354d819078289c6b574e95` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/ximalaya/ximalaya/ximalaya.json) |
| surge | `surge/ximalaya/ximalaya/ximalaya.list` | 5 | 157 | `f720fcca26e01aab3d1e52e6e616fc9ebddca01b9d6744d25e3e762665860ae7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/ximalaya/ximalaya/ximalaya.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/ximalaya/ximalaya/ximalaya.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/ximalaya/ximalaya/ximalaya.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/ximalaya/ximalaya/ximalaya.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/ximalaya/ximalaya/ximalaya.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/ximalaya/ximalaya/ximalaya.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/ximalaya/ximalaya/ximalaya.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/ximalaya/ximalaya/ximalaya.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  ximalaya:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/ximalaya/ximalaya/ximalaya.yaml"
    path: ./ruleset/ximalaya.yaml
    interval: 86400

rules:
  - RULE-SET,ximalaya,PROXY
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