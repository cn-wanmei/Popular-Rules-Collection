<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/remix/service.svg" alt="Trip.com 图标" width="72" height="72">

# Trip.com — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `ctrip` |
| 类型 | service |
| Provider / 服务集 | `ctrip` |
| 规则浏览路径 | `ctrip/ctrip/ctrip.yaml` |
| 语义规则数量 | **29** |
| 语义 SHA-256 | `a2db7f7c5f554f6dce66f7ed3d48d2d1b8bd51be863a5c2f19bf93846c16af63` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标：**remix semantic fallback**

- Style：`remix`
- Identity：`semantic.fallback.remix`
- 本地 V4 Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/remix/service.svg`
- 语义：仅用于完整覆盖规则服务，不代表官方品牌 Logo。

风格层参考：Lucide / Tabler / Phosphor / Material Symbols / Fluent UI / Heroicons / Remix / Bootstrap / Solar。

## 3. 服务集与层级

所属服务集：[ctrip](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/ctrip/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/ctrip/ctrip/ctrip.yaml` | 29 | 532 | `fd9923959b5e10b0448b3e298cb25e407004b77b7b46054da8914cfe9f9fe97d` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/ctrip/ctrip/ctrip.yaml) |
| loon | `loon/ctrip/ctrip/ctrip.list` | 29 | 745 | `c3d7e2594ae4fa10a4e65342fac7f25b3ab355a8d407598efe9e14e14ea9982c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/ctrip/ctrip/ctrip.list) |
| mihomo | `mihomo/ctrip/ctrip/ctrip.yaml` | 29 | 870 | `d775d7fbd08aead2b23bfbfe326b4428a3a191c9deb8bb672da810f1f3624b1b` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/ctrip/ctrip/ctrip.yaml) |
| quantumultx | `quantumultx/ctrip/ctrip/ctrip.list` | 29 | 919 | `7830e882e0ce87d9361143a05481c04317de30e465bbe1e0fba834120bc7af40` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/ctrip/ctrip/ctrip.list) |
| shadowrocket | `shadowrocket/ctrip/ctrip/ctrip.list` | 29 | 745 | `c3d7e2594ae4fa10a4e65342fac7f25b3ab355a8d407598efe9e14e14ea9982c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/ctrip/ctrip/ctrip.list) |
| singbox | `singbox/ctrip/ctrip/ctrip.json` | 0 | 739 | `a195ce0898984b890b3b18111bc0864701a56028b23faf327f7d6c27b0e2cd69` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/ctrip/ctrip/ctrip.json) |
| surge | `surge/ctrip/ctrip/ctrip.list` | 29 | 745 | `c3d7e2594ae4fa10a4e65342fac7f25b3ab355a8d407598efe9e14e14ea9982c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/ctrip/ctrip/ctrip.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/ctrip/ctrip/ctrip.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/ctrip/ctrip/ctrip.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/ctrip/ctrip/ctrip.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/ctrip/ctrip/ctrip.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/ctrip/ctrip/ctrip.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/ctrip/ctrip/ctrip.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/ctrip/ctrip/ctrip.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  ctrip:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/ctrip/ctrip/ctrip.yaml"
    path: ./ruleset/ctrip.yaml
    interval: 86400

rules:
  - RULE-SET,ctrip,PROXY
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