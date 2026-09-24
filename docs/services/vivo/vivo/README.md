<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/vivo.png" alt="vivo 图标" width="72" height="72">

# vivo — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `vivo` |
| 类型 | service |
| Provider / 服务集 | `vivo` |
| 规则浏览路径 | `vivo/vivo/vivo.yaml` |
| 语义规则数量 | **14** |
| 语义 SHA-256 | `12b5d8915023ba7ca34ca2f18f41b35a5e698cca4f9e22d2e2301f311e2b21ba` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标：**Official / Brand Native**

- Identity：`brand.vivo`
- 来源：Current V3 已发布品牌身份资产
- Icon Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/vivo.png`
- Digest：`f09ccbbc7330d5c8a095503625e7a477049a98f86dfd664346d32b7a78e7f2cc`

本服务存在可信品牌身份，因此 V4 不使用九风格 fallback 重绘该品牌 Logo。

风格层参考：Lucide / Tabler / Phosphor / Material Symbols / Fluent UI / Heroicons / Remix / Bootstrap / Solar。

## 3. 服务集与层级

所属服务集：[vivo](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/vivo/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/vivo/vivo/vivo.yaml` | 14 | 258 | `0cf2d8e071427b31c9a6e071255ca1b8a0424ad5e5a6bfa386a474e68e2e81e3` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/vivo/vivo/vivo.yaml) |
| loon | `loon/vivo/vivo/vivo.list` | 14 | 351 | `a938c5e0820f3358dfc7ce16e4988687244ac64adf2ef954cac7eceb2fac7892` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/vivo/vivo/vivo.list) |
| mihomo | `mihomo/vivo/vivo/vivo.yaml` | 14 | 416 | `c635ce22f118fcb3eb896116d5c1ddc3e7418b1e5f5df0f12b5e2ab906131b40` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/vivo/vivo/vivo.yaml) |
| quantumultx | `quantumultx/vivo/vivo/vivo.list` | 14 | 435 | `9cef4a73bf7914c22bcaac78f87a65a119bd1692c1780a4e54321dcc5171f2f7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/vivo/vivo/vivo.list) |
| shadowrocket | `shadowrocket/vivo/vivo/vivo.list` | 14 | 351 | `a938c5e0820f3358dfc7ce16e4988687244ac64adf2ef954cac7eceb2fac7892` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/vivo/vivo/vivo.list) |
| singbox | `singbox/vivo/vivo/vivo.json` | 0 | 390 | `fb43f7cf3013ffa29f11720d4889f78bcddcf6bb7f8b3491011b185c31ef3c04` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/vivo/vivo/vivo.json) |
| surge | `surge/vivo/vivo/vivo.list` | 14 | 351 | `a938c5e0820f3358dfc7ce16e4988687244ac64adf2ef954cac7eceb2fac7892` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/vivo/vivo/vivo.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/vivo/vivo/vivo.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/vivo/vivo/vivo.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/vivo/vivo/vivo.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/vivo/vivo/vivo.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/vivo/vivo/vivo.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/vivo/vivo/vivo.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/vivo/vivo/vivo.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  vivo:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/vivo/vivo/vivo.yaml"
    path: ./ruleset/vivo.yaml
    interval: 86400

rules:
  - RULE-SET,vivo,PROXY
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