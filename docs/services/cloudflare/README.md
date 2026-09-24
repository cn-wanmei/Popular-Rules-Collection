<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/cloudflare.png" alt="Cloudflare 图标" width="72" height="72">

# Cloudflare — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `cloudflare` |
| 类型 | provider_aggregate |
| Provider / 服务集 | `cloudflare` |
| 规则浏览路径 | `cloudflare/cloudflare.yaml` |
| 语义规则数量 | **98** |
| 语义 SHA-256 | `4d3cbb1a8e0ba731b7d79c1b90c6a37d308d8a587e09e96e2d69df39d9ddcf35` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标：**Official / Brand Native**

- Identity：`brand.cloudflare`
- 来源：Current V3 已发布品牌身份资产
- Icon Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/cloudflare.png`
- Digest：`8649a1dd6e186ff00958ec722dda105dd5ed981aea88e1f887394e6089860404`

本服务存在可信品牌身份，因此 V4 不使用九风格 fallback 重绘该品牌 Logo。

风格层参考：Lucide / Tabler / Phosphor / Material Symbols / Fluent UI / Heroicons / Remix / Bootstrap / Solar。

## 3. 服务集与层级

所属服务集：[cloudflare](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/cloudflare/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/cloudflare/cloudflare.yaml` | 98 | 2307 | `e08b65375b7dc494c9f82f7e85c54be790a12998a54b92f22af3f30c4f05dde5` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/cloudflare/cloudflare.yaml) |
| loon | `loon/cloudflare/cloudflare.list` | 98 | 2920 | `e7d45de73cbec3aeb2e50cc768a938413bb049968661555abf346d75ab54163a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/cloudflare/cloudflare.list) |
| mihomo | `mihomo/cloudflare/cloudflare.yaml` | 98 | 3321 | `cbed116454ccb6c19418744441b19ff7826d2fe4f19031116a39309de06065ef` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/cloudflare/cloudflare.yaml) |
| quantumultx | `quantumultx/cloudflare/cloudflare.list` | 98 | 3552 | `38c654c361e0d911f3bc093983161379cc324b4268c37cc4f4c42ef03c86c94a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/cloudflare/cloudflare.list) |
| shadowrocket | `shadowrocket/cloudflare/cloudflare.list` | 98 | 2920 | `e7d45de73cbec3aeb2e50cc768a938413bb049968661555abf346d75ab54163a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/cloudflare/cloudflare.list) |
| singbox | `singbox/cloudflare/cloudflare.json` | 0 | 2859 | `f9f3ffcedbde83b9e30ed845866d43b27fb19139958e6a13407ad0da42093e70` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/cloudflare/cloudflare.json) |
| surge | `surge/cloudflare/cloudflare.list` | 98 | 2920 | `e7d45de73cbec3aeb2e50cc768a938413bb049968661555abf346d75ab54163a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/cloudflare/cloudflare.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/cloudflare/cloudflare.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/cloudflare/cloudflare.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/cloudflare/cloudflare.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/cloudflare/cloudflare.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/cloudflare/cloudflare.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/cloudflare/cloudflare.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/cloudflare/cloudflare.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  cloudflare:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/cloudflare/cloudflare.yaml"
    path: ./ruleset/cloudflare.yaml
    interval: 86400

rules:
  - RULE-SET,cloudflare,PROXY
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