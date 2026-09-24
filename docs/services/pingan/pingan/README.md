<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/fluent/service.svg" alt="Ping An 图标" width="72" height="72">

# Ping An — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `pingan` |
| 类型 | service |
| Provider / 服务集 | `pingan` |
| 规则浏览路径 | `pingan/pingan/pingan.yaml` |
| 语义规则数量 | **27** |
| 语义 SHA-256 | `fe6a2b6d029369602eb5d8fd93d1f0c123d2fce1bb81640a2eca185f1eaa6179` |
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

所属服务集：[pingan](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/pingan/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/pingan/pingan/pingan.yaml` | 27 | 540 | `66fec963bb623d2aeea96fed8f852c226174d0c129b6b7b2fc3e4716587fc737` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/pingan/pingan/pingan.yaml) |
| loon | `loon/pingan/pingan/pingan.list` | 27 | 737 | `9dfad52328d184592ee23855fa153752256b1ef8338b6a3f332440e090aa29e0` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/pingan/pingan/pingan.list) |
| mihomo | `mihomo/pingan/pingan/pingan.yaml` | 27 | 854 | `1f0e309010443bacab05593d2c47fb1440d779a87d8ad59f589e9c26511912d5` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/pingan/pingan/pingan.yaml) |
| quantumultx | `quantumultx/pingan/pingan/pingan.list` | 27 | 899 | `56b11ed07c1a4efcbfb922e0d8ac55e58d27d835de5e8417a822e736d9d29456` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/pingan/pingan/pingan.list) |
| shadowrocket | `shadowrocket/pingan/pingan/pingan.list` | 27 | 737 | `9dfad52328d184592ee23855fa153752256b1ef8338b6a3f332440e090aa29e0` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/pingan/pingan/pingan.list) |
| singbox | `singbox/pingan/pingan/pingan.json` | 0 | 737 | `90d7b22c384ca6d60ab397d49412577c7575853e44e8652eff182e9ce32b614e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/pingan/pingan/pingan.json) |
| surge | `surge/pingan/pingan/pingan.list` | 27 | 737 | `9dfad52328d184592ee23855fa153752256b1ef8338b6a3f332440e090aa29e0` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/pingan/pingan/pingan.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/pingan/pingan/pingan.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/pingan/pingan/pingan.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/pingan/pingan/pingan.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/pingan/pingan/pingan.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/pingan/pingan/pingan.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/pingan/pingan/pingan.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/pingan/pingan/pingan.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  pingan:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/pingan/pingan/pingan.yaml"
    path: ./ruleset/pingan.yaml
    interval: 86400

rules:
  - RULE-SET,pingan,PROXY
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