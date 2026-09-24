<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/tabler/service.svg" alt="Ele.me 图标" width="72" height="72">

# Ele.me — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `eleme` |
| 类型 | service |
| Provider / 服务集 | `alibaba` |
| 规则浏览路径 | `alibaba/eleme/eleme.yaml` |
| 语义规则数量 | **13** |
| 语义 SHA-256 | `df0e6e9cfd914f85c76f94fd7c23ff2fe009482bb1eef06023f32b2de6d0cd27` |
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

所属服务集：[alibaba](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/alibaba/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/alibaba/eleme/eleme.yaml` | 13 | 259 | `2a568a652fd884ac97f4203caad0a8f509ca13b254f3e47667a5495bf62fde75` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/alibaba/eleme/eleme.yaml) |
| loon | `loon/alibaba/eleme/eleme.list` | 13 | 344 | `e2e25b8f85866b1cf86c6c4b960cc683f68dffe6cb909846a4c6ab18882ba732` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/alibaba/eleme/eleme.list) |
| mihomo | `mihomo/alibaba/eleme/eleme.yaml` | 13 | 405 | `6364ca9cc6acdb40a947674437e32ea16dbd2f257b851d4f8f2cdb749b9f1483` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/alibaba/eleme/eleme.yaml) |
| quantumultx | `quantumultx/alibaba/eleme/eleme.list` | 13 | 422 | `e75063a445d4888f2596d08aa3c4575882f18c4610fd8a624e1464e4af36de4a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/alibaba/eleme/eleme.list) |
| shadowrocket | `shadowrocket/alibaba/eleme/eleme.list` | 13 | 344 | `e2e25b8f85866b1cf86c6c4b960cc683f68dffe6cb909846a4c6ab18882ba732` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/alibaba/eleme/eleme.list) |
| singbox | `singbox/alibaba/eleme/eleme.json` | 0 | 386 | `d4374262eb9bad52c8de1f202f458ac9c388b82ddeff015c52c371316ffcc52b` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/alibaba/eleme/eleme.json) |
| surge | `surge/alibaba/eleme/eleme.list` | 13 | 344 | `e2e25b8f85866b1cf86c6c4b960cc683f68dffe6cb909846a4c6ab18882ba732` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/alibaba/eleme/eleme.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/alibaba/eleme/eleme.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/alibaba/eleme/eleme.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/alibaba/eleme/eleme.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/alibaba/eleme/eleme.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/alibaba/eleme/eleme.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/alibaba/eleme/eleme.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/alibaba/eleme/eleme.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  eleme:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/alibaba/eleme/eleme.yaml"
    path: ./ruleset/eleme.yaml
    interval: 86400

rules:
  - RULE-SET,eleme,PROXY
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