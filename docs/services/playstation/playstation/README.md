<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/playstation.png" alt="PlayStation 图标" width="72" height="72">

# PlayStation — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `playstation` |
| 类型 | service |
| Provider / 服务集 | `playstation` |
| 规则浏览路径 | `playstation/playstation/playstation.yaml` |
| 语义规则数量 | **4** |
| 语义 SHA-256 | `160449d533de2fd786a2c3d2d575b4df1b0c3bab1444afb2125afcbe031ba0e7` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标：**Official / Brand Native**

- Identity：`brand.playstation`
- 来源：Current V3 已发布品牌身份资产
- Icon Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/playstation.png`
- Digest：`0f6cdc50fdfb3a27a7c80dcbf361bebb9e9cada417276828196444e22d4eed80`

本服务存在可信品牌身份，因此 V4 不使用九风格 fallback 重绘该品牌 Logo。

风格层参考：Lucide / Tabler / Phosphor / Material Symbols / Fluent UI / Heroicons / Remix / Bootstrap / Solar。

## 3. 服务集与层级

所属服务集：[playstation](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/playstation/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/playstation/playstation/playstation.yaml` | 4 | 127 | `de94e368df138979b309f7f1cd0591c2aa5b00ebb4df6f397a25a7d3906069cc` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/playstation/playstation/playstation.yaml) |
| loon | `loon/playstation/playstation/playstation.list` | 4 | 140 | `7ea8a5184a0c0eb7f2ffbeb6a7e6117f6cb4e34b9f4da03cb7a610ae694a66f6` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/playstation/playstation/playstation.list) |
| mihomo | `mihomo/playstation/playstation/playstation.yaml` | 4 | 165 | `2f1a0803b7223f6ac6154f3515efd74aceab9b4822778df6b65cf390a03428ed` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/playstation/playstation/playstation.yaml) |
| quantumultx | `quantumultx/playstation/playstation/playstation.list` | 4 | 164 | `ff89f81774705a628cfd91e253a2dcf970d82c32d397ed2acf10e003cbb250da` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/playstation/playstation/playstation.list) |
| shadowrocket | `shadowrocket/playstation/playstation/playstation.list` | 4 | 140 | `7ea8a5184a0c0eb7f2ffbeb6a7e6117f6cb4e34b9f4da03cb7a610ae694a66f6` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/playstation/playstation/playstation.list) |
| singbox | `singbox/playstation/playstation/playstation.json` | 0 | 209 | `11efcdcb3efc47cba292d82c7de523f84833b228745e1f5a4788f3c3f432c515` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/playstation/playstation/playstation.json) |
| surge | `surge/playstation/playstation/playstation.list` | 4 | 140 | `7ea8a5184a0c0eb7f2ffbeb6a7e6117f6cb4e34b9f4da03cb7a610ae694a66f6` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/playstation/playstation/playstation.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/playstation/playstation/playstation.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/playstation/playstation/playstation.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/playstation/playstation/playstation.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/playstation/playstation/playstation.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/playstation/playstation/playstation.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/playstation/playstation/playstation.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/playstation/playstation/playstation.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  playstation:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/playstation/playstation/playstation.yaml"
    path: ./ruleset/playstation.yaml
    interval: 86400

rules:
  - RULE-SET,playstation,PROXY
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