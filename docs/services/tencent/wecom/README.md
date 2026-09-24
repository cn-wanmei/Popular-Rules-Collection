<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/heroicons/service.svg" alt="WeCom 图标" width="72" height="72">

# WeCom — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `wecom` |
| 类型 | service |
| Provider / 服务集 | `tencent` |
| 规则浏览路径 | `tencent/wecom/wecom.yaml` |
| 语义规则数量 | **3** |
| 语义 SHA-256 | `4a18e1c73ff9322f6c038c3e213b5e1e4b00c9e6400d0d9dd4dcc42d1ec745d6` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标：**heroicons semantic fallback**

- Style：`heroicons`
- Identity：`semantic.fallback.heroicons`
- 本地 V4 Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/heroicons/service.svg`
- 语义：仅用于完整覆盖规则服务，不代表官方品牌 Logo。

风格层参考：Lucide / Tabler / Phosphor / Material Symbols / Fluent UI / Heroicons / Remix / Bootstrap / Solar。

## 3. 服务集与层级

所属服务集：[tencent](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/tencent/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/tencent/wecom/wecom.yaml` | 3 | 109 | `99635f5e2b60092d7d079cd52a104e5ea1cf4554aeab8487aeb2c422b811d644` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/tencent/wecom/wecom.yaml) |
| loon | `loon/tencent/wecom/wecom.list` | 3 | 114 | `a02cf0a9280a3a577ec647ad6f870be53a581bcb3630d812ea11b7dd6a527154` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/tencent/wecom/wecom.list) |
| mihomo | `mihomo/tencent/wecom/wecom.yaml` | 3 | 135 | `4722eb7c28bc9efcde291e9c7ad3522105e69c808dc82af90581cbf1dc8a51c9` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/tencent/wecom/wecom.yaml) |
| quantumultx | `quantumultx/tencent/wecom/wecom.list` | 3 | 132 | `38bd791aa327ffc8691d3bbf39c320fd9c7c72642a38e58d1532ee2300c98be4` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/tencent/wecom/wecom.list) |
| shadowrocket | `shadowrocket/tencent/wecom/wecom.list` | 3 | 114 | `a02cf0a9280a3a577ec647ad6f870be53a581bcb3630d812ea11b7dd6a527154` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/tencent/wecom/wecom.list) |
| singbox | `singbox/tencent/wecom/wecom.json` | 0 | 186 | `bb53adab88d56a48940ec6092585a2c48a53bf095fed66343980a967c37fe85d` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/tencent/wecom/wecom.json) |
| surge | `surge/tencent/wecom/wecom.list` | 3 | 114 | `a02cf0a9280a3a577ec647ad6f870be53a581bcb3630d812ea11b7dd6a527154` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/tencent/wecom/wecom.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/tencent/wecom/wecom.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/tencent/wecom/wecom.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/tencent/wecom/wecom.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/tencent/wecom/wecom.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/tencent/wecom/wecom.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/tencent/wecom/wecom.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/tencent/wecom/wecom.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  wecom:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/tencent/wecom/wecom.yaml"
    path: ./ruleset/wecom.yaml
    interval: 86400

rules:
  - RULE-SET,wecom,PROXY
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