<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/anthropic.png" alt="Anthropic 图标" width="72" height="72">

# Anthropic — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `anthropic` |
| 类型 | service |
| Provider / 服务集 | `anthropic` |
| 规则浏览路径 | `anthropic/anthropic/anthropic.yaml` |
| 语义规则数量 | **9** |
| 语义 SHA-256 | `3975be18851d98eca3653a7eb5aadd2e918107293fb222642a484d2e69c2b500` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标：**Official / Brand Native**

- Identity：`brand.anthropic`
- 来源：Current V3 已发布品牌身份资产
- Icon Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/anthropic.png`
- Digest：`eb234ca13dcb65281d3fda9aa26529b0b24e6f3c45f7a69b313ad1884ddd72d1`

本服务存在可信品牌身份，因此 V4 不使用九风格 fallback 重绘该品牌 Logo。

风格层参考：Lucide / Tabler / Phosphor / Material Symbols / Fluent UI / Heroicons / Remix / Bootstrap / Solar。

## 3. 服务集与层级

所属服务集：[anthropic](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/anthropic/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/anthropic/anthropic/anthropic.yaml` | 19 | 483 | `869e98a5819f777236f974f918f944c344f78760059aba11165d30f4871381d5` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/anthropic/anthropic/anthropic.yaml) |
| loon | `loon/anthropic/anthropic/anthropic.list` | 19 | 590 | `c331884b8f58e25c6762d626c11a30ca63243b446daabf53427282370012e5ac` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/anthropic/anthropic/anthropic.list) |
| mihomo | `mihomo/anthropic/anthropic/anthropic.yaml` | 19 | 675 | `f658a9b432137cb06dea155c2117c6b5a86578ae4cc23ae6c0330eda06d994a1` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/anthropic/anthropic/anthropic.yaml) |
| quantumultx | `quantumultx/anthropic/anthropic/anthropic.list` | 19 | 704 | `07e62b966628fe2d17d138b25b86c39326940635057d486b41e8684677e7771b` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/anthropic/anthropic/anthropic.list) |
| shadowrocket | `shadowrocket/anthropic/anthropic/anthropic.list` | 19 | 590 | `c331884b8f58e25c6762d626c11a30ca63243b446daabf53427282370012e5ac` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/anthropic/anthropic/anthropic.list) |
| singbox | `singbox/anthropic/anthropic/anthropic.json` | 0 | 654 | `ef8dcc679b6a424cfd364a9d16335130faedd36d159855fd9ace447ad9a139ef` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/anthropic/anthropic/anthropic.json) |
| surge | `surge/anthropic/anthropic/anthropic.list` | 19 | 590 | `c331884b8f58e25c6762d626c11a30ca63243b446daabf53427282370012e5ac` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/anthropic/anthropic/anthropic.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/anthropic/anthropic/anthropic.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/anthropic/anthropic/anthropic.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/anthropic/anthropic/anthropic.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/anthropic/anthropic/anthropic.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/anthropic/anthropic/anthropic.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/anthropic/anthropic/anthropic.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/anthropic/anthropic/anthropic.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  anthropic:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/anthropic/anthropic/anthropic.yaml"
    path: ./ruleset/anthropic.yaml
    interval: 86400

rules:
  - RULE-SET,anthropic,PROXY
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