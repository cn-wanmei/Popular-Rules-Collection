<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/tabler/service.svg" alt="Tencent Cloud 图标" width="72" height="72">

# Tencent Cloud — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `tencentcloud` |
| 类型 | service |
| Provider / 服务集 | `tencent` |
| 规则浏览路径 | `tencent/tencentcloud/tencentcloud.yaml` |
| 语义规则数量 | **105** |
| 语义 SHA-256 | `601e2b8ab623be8677d8797c6a10330b2c599e8a2e53283dd28075dcd3b0ef19` |
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

所属服务集：[tencent](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/tencent/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/tencent/tencentcloud/tencentcloud.yaml` | 105 | 2290 | `ce1eda3fd4c5770b616180d4389fe8235181cf5420a4ffe0414a8a8549083b66` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/tencent/tencentcloud/tencentcloud.yaml) |
| loon | `loon/tencent/tencentcloud/tencentcloud.list` | 105 | 2462 | `e2840790020927d91206298d48d2ae637593d187d1456cf4513cc5874d57b8d0` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/tencent/tencentcloud/tencentcloud.list) |
| mihomo | `mihomo/tencent/tencentcloud/tencentcloud.yaml` | 105 | 2891 | `4a14d5b0b8978bce24f2b664b96bd46cdd4192b8c7578320b81cf59988d8d114` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/tencent/tencentcloud/tencentcloud.yaml) |
| quantumultx | `quantumultx/tencent/tencentcloud/tencentcloud.list` | 105 | 3300 | `015135393d8f54ff2db1aca6810fd65567c3bb9ed59b8b1e28ffdf7d731f4dd3` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/tencent/tencentcloud/tencentcloud.list) |
| shadowrocket | `shadowrocket/tencent/tencentcloud/tencentcloud.list` | 105 | 2462 | `e2840790020927d91206298d48d2ae637593d187d1456cf4513cc5874d57b8d0` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/tencent/tencentcloud/tencentcloud.list) |
| singbox | `singbox/tencent/tencentcloud/tencentcloud.json` | 0 | 2877 | `ac781f4eb2747c973be9882980dc640855a33a70ae8978c04097fd8ef7048e47` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/tencent/tencentcloud/tencentcloud.json) |
| surge | `surge/tencent/tencentcloud/tencentcloud.list` | 105 | 2462 | `e2840790020927d91206298d48d2ae637593d187d1456cf4513cc5874d57b8d0` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/tencent/tencentcloud/tencentcloud.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/tencent/tencentcloud/tencentcloud.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/tencent/tencentcloud/tencentcloud.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/tencent/tencentcloud/tencentcloud.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/tencent/tencentcloud/tencentcloud.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/tencent/tencentcloud/tencentcloud.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/tencent/tencentcloud/tencentcloud.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/tencent/tencentcloud/tencentcloud.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  tencentcloud:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/tencent/tencentcloud/tencentcloud.yaml"
    path: ./ruleset/tencentcloud.yaml
    interval: 86400

rules:
  - RULE-SET,tencentcloud,PROXY
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