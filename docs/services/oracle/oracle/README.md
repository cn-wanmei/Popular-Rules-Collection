<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/oracle.png" alt="Oracle 图标" width="72" height="72">

# Oracle — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `oracle` |
| 类型 | service |
| Provider / 服务集 | `oracle` |
| 规则浏览路径 | `oracle/oracle/oracle.yaml` |
| 语义规则数量 | **27** |
| 语义 SHA-256 | `96f687811ff98ccf5ad4e8385226419786c842663ac357018c5ab2843776b4d9` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标：**Official / Brand Native**

- Identity：`brand.oracle`
- 来源：Current V3 已发布品牌身份资产
- Icon Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/oracle.png`
- Digest：`87cfa17000cd44818cf4c003eb10fcd612c16997e7b39df1a1f28dabf63810b8`

本服务存在可信品牌身份，因此 V4 不使用九风格 fallback 重绘该品牌 Logo。

风格层参考：Lucide / Tabler / Phosphor / Material Symbols / Fluent UI / Heroicons / Remix / Bootstrap / Solar。

## 3. 服务集与层级

所属服务集：[oracle](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/oracle/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/oracle/oracle/oracle.yaml` | 37 | 829 | `2aedc4d069d76581d400372ee1129e3025c99c679a054f1b2353357b5c6fce1c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/oracle/oracle/oracle.yaml) |
| loon | `loon/oracle/oracle/oracle.list` | 37 | 1088 | `eb1800833f308c630c63cbc7cd9d90785c5c63d080d313232b36a020d62ae9d1` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/oracle/oracle/oracle.list) |
| mihomo | `mihomo/oracle/oracle/oracle.yaml` | 37 | 1245 | `65f27dd6c3cf99b79a9a713f6bfa8760485c84888b816c436005597a709cb76e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/oracle/oracle/oracle.yaml) |
| quantumultx | `quantumultx/oracle/oracle/oracle.list` | 37 | 1310 | `76664ec368b494e7e4af55180f5fa5cc97a458b0dc3f0b861ab34b5ae3cc3516` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/oracle/oracle/oracle.list) |
| shadowrocket | `shadowrocket/oracle/oracle/oracle.list` | 37 | 1088 | `eb1800833f308c630c63cbc7cd9d90785c5c63d080d313232b36a020d62ae9d1` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/oracle/oracle/oracle.list) |
| singbox | `singbox/oracle/oracle/oracle.json` | 0 | 1090 | `afa4372b43f671324e393966099ea7229b9401269df123e88870f38aeb3e6a8a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/oracle/oracle/oracle.json) |
| surge | `surge/oracle/oracle/oracle.list` | 37 | 1088 | `eb1800833f308c630c63cbc7cd9d90785c5c63d080d313232b36a020d62ae9d1` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/oracle/oracle/oracle.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/oracle/oracle/oracle.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/oracle/oracle/oracle.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/oracle/oracle/oracle.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/oracle/oracle/oracle.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/oracle/oracle/oracle.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/oracle/oracle/oracle.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/oracle/oracle/oracle.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  oracle:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/oracle/oracle/oracle.yaml"
    path: ./ruleset/oracle.yaml
    interval: 86400

rules:
  - RULE-SET,oracle,PROXY
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