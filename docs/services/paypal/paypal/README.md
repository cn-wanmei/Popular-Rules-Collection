<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/paypal.png" alt="PayPal 图标" width="72" height="72">

# PayPal — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `paypal` |
| 类型 | service |
| Provider / 服务集 | `paypal` |
| 规则浏览路径 | `paypal/paypal/paypal.yaml` |
| 语义规则数量 | **247** |
| 语义 SHA-256 | `f2400b4567e1afe3fe79b71e75aaf13ded2144be478e6475ad07a139c43b2e43` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标：**Official / Brand Native**

- Identity：`brand.paypal`
- 来源：Current V3 已发布品牌身份资产
- Icon Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/paypal.png`
- Digest：`ce51f54524ca09f7b13ef53ecf9a70c7a011a0878642a4066bfe03dd27664d71`

本服务存在可信品牌身份，因此 V4 不使用九风格 fallback 重绘该品牌 Logo。

风格层参考：Lucide / Tabler / Phosphor / Material Symbols / Fluent UI / Heroicons / Remix / Bootstrap / Solar。

## 3. 服务集与层级

所属服务集：[paypal](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/paypal/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/paypal/paypal/paypal.yaml` | 250 | 5761 | `3853bcbe53fc186b1916177f4d18e0b90d870bb1a42d4d505b22e6b145934f21` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/paypal/paypal/paypal.yaml) |
| loon | `loon/paypal/paypal/paypal.list` | 250 | 7724 | `b060b134a189776197e515af702c89cdc00356610a6b2fbd4e5c5a6c15570633` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/paypal/paypal/paypal.list) |
| mihomo | `mihomo/paypal/paypal/paypal.yaml` | 250 | 8733 | `fe61ffb12cfe3c5334708ec3d6d2a4194429763cde423bf0c1247b075aab9564` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/paypal/paypal/paypal.yaml) |
| quantumultx | `quantumultx/paypal/paypal/paypal.list` | 250 | 9224 | `1d58617efcd882b6020de2b45b4ca9a1043e7c4eb98e0eee46c0e93099ea2c7f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/paypal/paypal/paypal.list) |
| shadowrocket | `shadowrocket/paypal/paypal/paypal.list` | 250 | 7724 | `b060b134a189776197e515af702c89cdc00356610a6b2fbd4e5c5a6c15570633` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/paypal/paypal/paypal.list) |
| singbox | `singbox/paypal/paypal/paypal.json` | 0 | 7087 | `6426efd93c5ddf5c393c7244f22eded7b3b7d9cf947e12b43397ea699f1eb27c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/paypal/paypal/paypal.json) |
| surge | `surge/paypal/paypal/paypal.list` | 250 | 7724 | `b060b134a189776197e515af702c89cdc00356610a6b2fbd4e5c5a6c15570633` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/paypal/paypal/paypal.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/paypal/paypal/paypal.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/paypal/paypal/paypal.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/paypal/paypal/paypal.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/paypal/paypal/paypal.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/paypal/paypal/paypal.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/paypal/paypal/paypal.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/paypal/paypal/paypal.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  paypal:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/paypal/paypal/paypal.yaml"
    path: ./ruleset/paypal.yaml
    interval: 86400

rules:
  - RULE-SET,paypal,PROXY
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