<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/solar/service.svg" alt="China Construction Bank 图标" width="72" height="72">

# China Construction Bank — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `ccb` |
| 类型 | service |
| Provider / 服务集 | `ccb` |
| 规则浏览路径 | `ccb/ccb/ccb.yaml` |
| 语义规则数量 | **18** |
| 语义 SHA-256 | `923aab5c4383df1ab267f73e84980bc2ae57ab5599664c8e8428167a939bb060` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标：**solar semantic fallback**

- Style：`solar`
- Identity：`semantic.fallback.solar`
- 本地 V4 Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/solar/service.svg`
- 语义：仅用于完整覆盖规则服务，不代表官方品牌 Logo。

风格层参考：Lucide / Tabler / Phosphor / Material Symbols / Fluent UI / Heroicons / Remix / Bootstrap / Solar。

## 3. 服务集与层级

所属服务集：[ccb](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/ccb/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/ccb/ccb/ccb.yaml` | 18 | 359 | `9716c8cdb21fa69dfd23690cceeb6a695a01a86b47cb93f75d00c5976cd7236f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/ccb/ccb/ccb.yaml) |
| loon | `loon/ccb/ccb/ccb.list` | 18 | 484 | `4fbb42d559766a02752a129fd1443be36b012c13627b297d26e280ee62534269` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/ccb/ccb/ccb.list) |
| mihomo | `mihomo/ccb/ccb/ccb.yaml` | 18 | 565 | `4a93f03ddf89ad70b0a9001f601cecdeb091828bd0914e0d089fdb11283ce0f9` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/ccb/ccb/ccb.yaml) |
| quantumultx | `quantumultx/ccb/ccb/ccb.list` | 18 | 592 | `bee812fb9048e9da006f3ff316b5d36ab284b99fcdc313a197817a2a1d174a53` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/ccb/ccb/ccb.list) |
| shadowrocket | `shadowrocket/ccb/ccb/ccb.list` | 18 | 484 | `4fbb42d559766a02752a129fd1443be36b012c13627b297d26e280ee62534269` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/ccb/ccb/ccb.list) |
| singbox | `singbox/ccb/ccb/ccb.json` | 0 | 511 | `f9ec45a58202fa0e4e38e566ea32ce4956cc814ce969ebfbda7ff51e38f09188` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/ccb/ccb/ccb.json) |
| surge | `surge/ccb/ccb/ccb.list` | 18 | 484 | `4fbb42d559766a02752a129fd1443be36b012c13627b297d26e280ee62534269` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/ccb/ccb/ccb.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/ccb/ccb/ccb.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/ccb/ccb/ccb.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/ccb/ccb/ccb.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/ccb/ccb/ccb.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/ccb/ccb/ccb.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/ccb/ccb/ccb.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/ccb/ccb/ccb.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  ccb:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/ccb/ccb/ccb.yaml"
    path: ./ruleset/ccb.yaml
    interval: 86400

rules:
  - RULE-SET,ccb,PROXY
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