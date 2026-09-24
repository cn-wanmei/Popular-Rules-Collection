<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/fluent/service.svg" alt="ByteDance 图标" width="72" height="72">

# ByteDance — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `bytedance` |
| 类型 | provider_aggregate |
| Provider / 服务集 | `bytedance` |
| 规则浏览路径 | `bytedance/bytedance.yaml` |
| 语义规则数量 | **1082** |
| 语义 SHA-256 | `04fab94e04296c75ea6864e5531af5a15a6c8da7fe015b21482cfe522f9af6ae` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标：**fluent semantic fallback**

- Style：`fluent`
- Identity：`semantic.fallback.fluent`
- 本地 V4 Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/fluent/service.svg`
- 语义：仅用于完整覆盖规则服务，不代表官方品牌 Logo。

风格层参考：Lucide / Tabler / Phosphor / Material Symbols / Fluent UI / Heroicons / Remix / Bootstrap / Solar。

## 3. 服务集与层级

所属服务集：[bytedance](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/bytedance/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/bytedance/bytedance.yaml` | 1081 | 22845 | `ee09c1ad061e6cb1e8bae6f92e3d27c59e99af64abb561ea24645e011a5ba367` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/bytedance/bytedance.yaml) |
| loon | `loon/bytedance/bytedance.list` | 1081 | 31436 | `20465ed9d7b1961cfd1869bbabf1d9d143a2a9a6202bd29d302396a87fc48135` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/bytedance/bytedance.list) |
| mihomo | `mihomo/bytedance/bytedance.yaml` | 1081 | 35769 | `336a1f03b254782b9ced6532e189b55e76b1edb23fed9f72466791e25a513a52` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/bytedance/bytedance.yaml) |
| quantumultx | `quantumultx/bytedance/bytedance.list` | 1081 | 37924 | `2c2cfab4488a4b46dd223a145d8a3d9f6db0d75903f20a83035e798761a64265` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/bytedance/bytedance.list) |
| shadowrocket | `shadowrocket/bytedance/bytedance.list` | 1081 | 31436 | `20465ed9d7b1961cfd1869bbabf1d9d143a2a9a6202bd29d302396a87fc48135` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/bytedance/bytedance.list) |
| singbox | `singbox/bytedance/bytedance.json` | 0 | 28340 | `539d988198ecf12787f03f5383b5b5f73463e3904383e2563e7af1cab759241f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/bytedance/bytedance.json) |
| surge | `surge/bytedance/bytedance.list` | 1081 | 31436 | `20465ed9d7b1961cfd1869bbabf1d9d143a2a9a6202bd29d302396a87fc48135` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/bytedance/bytedance.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/bytedance/bytedance.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/bytedance/bytedance.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/bytedance/bytedance.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/bytedance/bytedance.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/bytedance/bytedance.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/bytedance/bytedance.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/bytedance/bytedance.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  bytedance:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/bytedance/bytedance.yaml"
    path: ./ruleset/bytedance.yaml
    interval: 86400

rules:
  - RULE-SET,bytedance,PROXY
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