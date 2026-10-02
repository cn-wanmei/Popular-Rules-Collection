<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Icon/dist/v/089c95447a0d6ae831f3c4369393fd029a5fba251858298ea08a667328212562.png" alt="service icon" width="72" height="72">

# Airbnb — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon System 6.0 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `airbnb_aggregate` |
| 类型 | provider_aggregate |
| Provider / 服务集 | `airbnb` |
| 规则浏览路径 | `airbnb/airbnb.yaml` |
| 语义规则数量 | **83** |
| 语义 SHA-256 | `16a2bb3a0cbad36218e7e760e3f0b8a241855f158eb41badcba6d60844f1d19c` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标：**Official / Brand Native**

- Identity：`brand.airbnb`
- 来源：Current V3 已发布品牌身份资产
- Icon Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Icon/dist/v/089c95447a0d6ae831f3c4369393fd029a5fba251858298ea08a667328212562.png
- Digest：`9c7037c8f417b7d1ed435d71552e9040c9d797fbee02a1eac100c0d1895f8edc`

本服务存在可信品牌身份，因此 V4 不使用九风格 fallback 重绘该品牌 Logo。

风格层：Icon V6 production styles（见 `config/variant-policy.yaml` / STYLE_SYSTEM_V1）。

## 3. 服务集与层级

所属服务集：[airbnb](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/airbnb/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/airbnb/airbnb.yaml` | 83 | 1499 | `d83a1d0e1358e3a983ea11e257261838330f37ca60927dcf2d49b27dbb295e22` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/airbnb/airbnb.yaml) |
| loon | `loon/airbnb/airbnb.list` | 83 | 2144 | `86f0fa2f798dbb7010b5883a5ed20e33e3b43151e138dc22c3a0e2cc002e2d3c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/airbnb/airbnb.list) |
| mihomo | `mihomo/airbnb/airbnb.yaml` | 83 | 2485 | `de30a0ec22805b4a4d86b31ad03d951ee53e6f3788250e571226fb9c5660f3c0` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/airbnb/airbnb.yaml) |
| quantumultx | `quantumultx/airbnb/airbnb.list` | 83 | 2642 | `b37916c83716f9d77d01bb43723e8aef6a24f75769245af4cd75ce50bd98e696` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/airbnb/airbnb.list) |
| shadowrocket | `shadowrocket/airbnb/airbnb.list` | 83 | 2144 | `86f0fa2f798dbb7010b5883a5ed20e33e3b43151e138dc22c3a0e2cc002e2d3c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/airbnb/airbnb.list) |
| singbox | `singbox/airbnb/airbnb.json` | 0 | 1976 | `1e82140d9a842f62aa555dd626fb73731ef34994bd6499a3baacbf2768741824` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/airbnb/airbnb.json) |
| surge | `surge/airbnb/airbnb.list` | 83 | 2144 | `86f0fa2f798dbb7010b5883a5ed20e33e3b43151e138dc22c3a0e2cc002e2d3c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/airbnb/airbnb.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/airbnb/airbnb.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/airbnb/airbnb.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/airbnb/airbnb.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/airbnb/airbnb.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/airbnb/airbnb.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/airbnb/airbnb.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/airbnb/airbnb.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  airbnb_aggregate:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/airbnb/airbnb.yaml"
    path: ./ruleset/airbnb_aggregate.yaml
    interval: 86400

rules:
  - RULE-SET,airbnb_aggregate,PROXY
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
| 当前 Icon 主层 | Icon V6 `icon-2026.09.30.clean1` |
| Icon Release | `icon-2026.09.30.clean1` |

统计口径：`rule_count` 是 Manifest 对客户端文件记录的字段，不同客户端可能有不同口径；服务本身的主要规则数量以 `rule/_index.yaml` 语义 `rule_count` 为准。

当前 Collection Date：`2026-09-24`；Release Generated At：`2026-09-24T04:39:15.367236+00:00`。

## 8. 相关入口

- [服务总目录](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/SERVICE_CATALOG.md)
- [Icon System 6.0](https://github.com/cn-wanmei/Popular-Rules-Icon)
- [V4 Style Guide](https://github.com/cn-wanmei/Popular-Rules-Icon)
- [完整规则使用说明](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/RULE_USAGE_GUIDE.md)
- [规则索引](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/rule/_index.yaml)

[回到顶部](#top)