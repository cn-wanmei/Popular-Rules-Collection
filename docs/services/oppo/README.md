<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/oppo.png" alt="OPPO 图标" width="72" height="72">

# OPPO — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `oppo_aggregate` |
| 类型 | provider_aggregate |
| Provider / 服务集 | `oppo` |
| 规则浏览路径 | `oppo/oppo.yaml` |
| 语义规则数量 | **56** |
| 语义 SHA-256 | `8efe8e148c5de0806d31dc4b924a405007f66156d817ddfa10781a0eb9a1ad7e` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标：**Official / Brand Native**

- Identity：`brand.oppo`
- 来源：Current V3 已发布品牌身份资产
- Icon Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/oppo.png`
- Digest：`537cc298378d3afa7790696ee168ec0138c8a97ba605ddf9970d031eb498e789`

本服务存在可信品牌身份，因此 V4 不使用九风格 fallback 重绘该品牌 Logo。

风格层参考：Lucide / Tabler / Phosphor / Material Symbols / Fluent UI / Heroicons / Remix / Bootstrap / Solar。

## 3. 服务集与层级

所属服务集：[oppo](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/oppo/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/oppo/oppo.yaml` | 56 | 1076 | `1612fcaafd4f94248bdb97782c2644d2b685fe41bd3fb4f37bcebf58e978030c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/oppo/oppo.yaml) |
| loon | `loon/oppo/oppo.list` | 56 | 1505 | `fb122e28c637f719a435d7207b54740065e5e4f1aa9b775b94014153308d4a0c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/oppo/oppo.list) |
| mihomo | `mihomo/oppo/oppo.yaml` | 56 | 1738 | `ad8f3b9090fa5e6cbcfb0395a65a3f9ea8fd7c38a9b7cb9ee6053ed48002a4de` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/oppo/oppo.yaml) |
| quantumultx | `quantumultx/oppo/oppo.list` | 56 | 1841 | `7f84e5bab5486cd3483aa3720fb2e2edf0321bac39763fc326bac872bf30754f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/oppo/oppo.list) |
| shadowrocket | `shadowrocket/oppo/oppo.list` | 56 | 1505 | `fb122e28c637f719a435d7207b54740065e5e4f1aa9b775b94014153308d4a0c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/oppo/oppo.list) |
| singbox | `singbox/oppo/oppo.json` | 0 | 1418 | `1e912dcb99e87fea57679a7b777d2fd2d322f4c9e3111df68ba080b83bfaef4f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/oppo/oppo.json) |
| surge | `surge/oppo/oppo.list` | 56 | 1505 | `fb122e28c637f719a435d7207b54740065e5e4f1aa9b775b94014153308d4a0c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/oppo/oppo.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/oppo/oppo.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/oppo/oppo.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/oppo/oppo.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/oppo/oppo.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/oppo/oppo.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/oppo/oppo.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/oppo/oppo.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  oppo_aggregate:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/oppo/oppo.yaml"
    path: ./ruleset/oppo_aggregate.yaml
    interval: 86400

rules:
  - RULE-SET,oppo_aggregate,PROXY
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