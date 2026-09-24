<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/soundcloud.png" alt="SoundCloud 图标" width="72" height="72">

# SoundCloud — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `soundcloud_aggregate` |
| 类型 | provider_aggregate |
| Provider / 服务集 | `soundcloud` |
| 规则浏览路径 | `soundcloud/soundcloud.yaml` |
| 语义规则数量 | **5** |
| 语义 SHA-256 | `d55ed6b4630b251af084915af87162df2a375571a13b1e708bb4592847d8eb74` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标：**Official / Brand Native**

- Identity：`brand.soundcloud`
- 来源：Current V3 已发布品牌身份资产
- Icon Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/soundcloud.png`
- Digest：`32095fc966027c27523b076e8680c0c9fa0237cf8270525936d5b2e7da3da9d1`

本服务存在可信品牌身份，因此 V4 不使用九风格 fallback 重绘该品牌 Logo。

风格层参考：Lucide / Tabler / Phosphor / Material Symbols / Fluent UI / Heroicons / Remix / Bootstrap / Solar。

## 3. 服务集与层级

所属服务集：[soundcloud](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/soundcloud/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/soundcloud/soundcloud.yaml` | 5 | 125 | `d8505d26d71330ad272415ec17789ab53791f59fc456e2422dd80b7c2e479d5b` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/soundcloud/soundcloud.yaml) |
| loon | `loon/soundcloud/soundcloud.list` | 5 | 146 | `b42a455a035f0f68541370393247e619724a5a597acb18d71813be3e2a945c24` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/soundcloud/soundcloud.list) |
| mihomo | `mihomo/soundcloud/soundcloud.yaml` | 5 | 175 | `ad5991a95fc7a7381b0d3069f65104f57c2eec336d261ac406535a6715918125` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/soundcloud/soundcloud.yaml) |
| quantumultx | `quantumultx/soundcloud/soundcloud.list` | 5 | 176 | `83554a4e1e97df7fa0a6abd801c38aa26c8a21a2503745b6c4b8aa43d3721a1e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/soundcloud/soundcloud.list) |
| shadowrocket | `shadowrocket/soundcloud/soundcloud.list` | 5 | 146 | `b42a455a035f0f68541370393247e619724a5a597acb18d71813be3e2a945c24` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/soundcloud/soundcloud.list) |
| singbox | `singbox/soundcloud/soundcloud.json` | 0 | 212 | `f2c161abea69993e8da943d9e73d7248c36ac176d7276ab0fee72bceabb557c1` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/soundcloud/soundcloud.json) |
| surge | `surge/soundcloud/soundcloud.list` | 5 | 146 | `b42a455a035f0f68541370393247e619724a5a597acb18d71813be3e2a945c24` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/soundcloud/soundcloud.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/soundcloud/soundcloud.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/soundcloud/soundcloud.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/soundcloud/soundcloud.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/soundcloud/soundcloud.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/soundcloud/soundcloud.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/soundcloud/soundcloud.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/soundcloud/soundcloud.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  soundcloud_aggregate:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/soundcloud/soundcloud.yaml"
    path: ./ruleset/soundcloud_aggregate.yaml
    interval: 86400

rules:
  - RULE-SET,soundcloud_aggregate,PROXY
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