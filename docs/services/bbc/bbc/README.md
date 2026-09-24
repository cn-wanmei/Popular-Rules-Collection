<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/bootstrap/service.svg" alt="BBC 图标" width="72" height="72">

# BBC — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `bbc` |
| 类型 | service |
| Provider / 服务集 | `bbc` |
| 规则浏览路径 | `bbc/bbc/bbc.yaml` |
| 语义规则数量 | **30** |
| 语义 SHA-256 | `0d063a54d8fecdf684eedcb9327dbed072680e4e9462e7fc49b0280b1a14da5d` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标：**bootstrap semantic fallback**

- Style：`bootstrap`
- Identity：`semantic.fallback.bootstrap`
- 本地 V4 Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/bootstrap/service.svg`
- 语义：仅用于完整覆盖规则服务，不代表官方品牌 Logo。

风格层参考：Lucide / Tabler / Phosphor / Material Symbols / Fluent UI / Heroicons / Remix / Bootstrap / Solar。

## 3. 服务集与层级

所属服务集：[bbc](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/bbc/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/bbc/bbc/bbc.yaml` | 37 | 914 | `8d9ea1964cb3c666cad3810847d6952fc1cc1539e3138c3912b8cec3e1c3de46` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/bbc/bbc/bbc.yaml) |
| loon | `loon/bbc/bbc/bbc.list` | 37 | 1086 | `44551c29fe9ec3ddc6d3fd73e2b27acc6db96db49c0caf75526dde8781a243a8` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/bbc/bbc/bbc.list) |
| mihomo | `mihomo/bbc/bbc/bbc.yaml` | 37 | 1243 | `f7cf72bf6aaf5ffac8fae1b14b4321a802c09d7d7c67658346bf191d9f74a7a7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/bbc/bbc/bbc.yaml) |
| quantumultx | `quantumultx/bbc/bbc/bbc.list` | 37 | 1308 | `410a3581b9efb33074ebf7414cc1c5f47a3f4404753eb41b413572ec38f2f6cc` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/bbc/bbc/bbc.list) |
| shadowrocket | `shadowrocket/bbc/bbc/bbc.list` | 37 | 1086 | `44551c29fe9ec3ddc6d3fd73e2b27acc6db96db49c0caf75526dde8781a243a8` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/bbc/bbc/bbc.list) |
| singbox | `singbox/bbc/bbc/bbc.json` | 0 | 1189 | `ad5a27e1058905dbea7e30a4a4428692d72e0b47d691a2835f3aef675a995da7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/bbc/bbc/bbc.json) |
| surge | `surge/bbc/bbc/bbc.list` | 37 | 1086 | `44551c29fe9ec3ddc6d3fd73e2b27acc6db96db49c0caf75526dde8781a243a8` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/bbc/bbc/bbc.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/bbc/bbc/bbc.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/bbc/bbc/bbc.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/bbc/bbc/bbc.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/bbc/bbc/bbc.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/bbc/bbc/bbc.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/bbc/bbc/bbc.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/bbc/bbc/bbc.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  bbc:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/bbc/bbc/bbc.yaml"
    path: ./ruleset/bbc.yaml
    interval: 86400

rules:
  - RULE-SET,bbc,PROXY
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