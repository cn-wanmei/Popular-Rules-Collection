<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/vercel.png" alt="Vercel 图标" width="72" height="72">

# Vercel — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `vercel` |
| 类型 | service |
| Provider / 服务集 | `vercel` |
| 规则浏览路径 | `vercel/vercel/vercel.yaml` |
| 语义规则数量 | **27** |
| 语义 SHA-256 | `b05758b97ee01304719bf91778de1fe3b1e35038fc1b5bdeeb68b79d8c1d5bb6` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标：**Official / Brand Native**

- Identity：`brand.vercel`
- 来源：Current V3 已发布品牌身份资产
- Icon Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/vercel.png`
- Digest：`4c3d1f713494edbf1c4dc048f322fb5d6facd95eb8e06aa8ebffe5c6e25eb44e`

本服务存在可信品牌身份，因此 V4 不使用九风格 fallback 重绘该品牌 Logo。

风格层参考：Lucide / Tabler / Phosphor / Material Symbols / Fluent UI / Heroicons / Remix / Bootstrap / Solar。

## 3. 服务集与层级

所属服务集：[vercel](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/vercel/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/vercel/vercel/vercel.yaml` | 27 | 521 | `afb5cad0c10317b6966ef5f644631124e74bc2baf66cf4eb0e9565dbcd1ac27d` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/vercel/vercel/vercel.yaml) |
| loon | `loon/vercel/vercel/vercel.list` | 27 | 718 | `71981a03db63d8a0cddc2da54b228fe5b23d8270e8c199f9a7159a64aa933768` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/vercel/vercel/vercel.list) |
| mihomo | `mihomo/vercel/vercel/vercel.yaml` | 27 | 835 | `2acaa2f010080dfd67b167edf01115c25a019ef75fe53b39fba83a164436b8ca` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/vercel/vercel/vercel.yaml) |
| quantumultx | `quantumultx/vercel/vercel/vercel.list` | 27 | 880 | `c233af68244682d7f25691701a26be7c2e156d4917b0d6d879491300acb01b2a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/vercel/vercel/vercel.list) |
| shadowrocket | `shadowrocket/vercel/vercel/vercel.list` | 27 | 718 | `71981a03db63d8a0cddc2da54b228fe5b23d8270e8c199f9a7159a64aa933768` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/vercel/vercel/vercel.list) |
| singbox | `singbox/vercel/vercel/vercel.json` | 0 | 718 | `a9a17f72c2ccc517e8c403b6309210866dcd41bd41a593d8c0c5ad68435973fd` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/vercel/vercel/vercel.json) |
| surge | `surge/vercel/vercel/vercel.list` | 27 | 718 | `71981a03db63d8a0cddc2da54b228fe5b23d8270e8c199f9a7159a64aa933768` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/vercel/vercel/vercel.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/vercel/vercel/vercel.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/vercel/vercel/vercel.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/vercel/vercel/vercel.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/vercel/vercel/vercel.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/vercel/vercel/vercel.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/vercel/vercel/vercel.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/vercel/vercel/vercel.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  vercel:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/vercel/vercel/vercel.yaml"
    path: ./ruleset/vercel.yaml
    interval: 86400

rules:
  - RULE-SET,vercel,PROXY
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