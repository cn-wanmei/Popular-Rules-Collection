<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/xiaomi.png" alt="Xiaomi 图标" width="72" height="72">

# Xiaomi — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `xiaomi` |
| 类型 | provider_aggregate |
| Provider / 服务集 | `xiaomi` |
| 规则浏览路径 | `xiaomi/xiaomi.yaml` |
| 语义规则数量 | **159** |
| 语义 SHA-256 | `089753b4ce48e8fd1a3ec568359696263d3a5e6c9b2a65fa03354de770feec5e` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标：**Official / Brand Native**

- Identity：`brand.xiaomi`
- 来源：Current V3 已发布品牌身份资产
- Icon Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/xiaomi.png`
- Digest：`a08a080236b4255034150bba68b849ed3adcd7f0daf29581a26d914fb56f792c`

本服务存在可信品牌身份，因此 V4 不使用九风格 fallback 重绘该品牌 Logo。

风格层参考：Lucide / Tabler / Phosphor / Material Symbols / Fluent UI / Heroicons / Remix / Bootstrap / Solar。

## 3. 服务集与层级

所属服务集：[xiaomi](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/xiaomi/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/xiaomi/xiaomi.yaml` | 157 | 3239 | `9c1fd9283e5706b5efaee32f18d135cf473066ef4b8ad7785bd7dad667805d6c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/xiaomi/xiaomi.yaml) |
| loon | `loon/xiaomi/xiaomi.list` | 157 | 4409 | `c2f8dd097a98adcc2bdba503fdd3dd7e25ec96121f78d100bb240a814e9245d9` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/xiaomi/xiaomi.list) |
| mihomo | `mihomo/xiaomi/xiaomi.yaml` | 157 | 5046 | `cc4545047d1a6073f1ff2e95d2cb9315c8f23178a0d22901af9dc3e28297babd` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/xiaomi/xiaomi.yaml) |
| quantumultx | `quantumultx/xiaomi/xiaomi.list` | 157 | 5369 | `efab0498a0f6fb7c4198e85fd25f5e866530ea2bfe1667abe1d5c0a7e2aabb85` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/xiaomi/xiaomi.list) |
| shadowrocket | `shadowrocket/xiaomi/xiaomi.list` | 157 | 4409 | `c2f8dd097a98adcc2bdba503fdd3dd7e25ec96121f78d100bb240a814e9245d9` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/xiaomi/xiaomi.list) |
| singbox | `singbox/xiaomi/xiaomi.json` | 0 | 4100 | `b69b64933ae8bbd5fa819e1a43db3bd669fa7bf42096cf811250900ca09e02ca` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/xiaomi/xiaomi.json) |
| surge | `surge/xiaomi/xiaomi.list` | 157 | 4409 | `c2f8dd097a98adcc2bdba503fdd3dd7e25ec96121f78d100bb240a814e9245d9` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/xiaomi/xiaomi.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/xiaomi/xiaomi.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/xiaomi/xiaomi.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/xiaomi/xiaomi.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/xiaomi/xiaomi.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/xiaomi/xiaomi.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/xiaomi/xiaomi.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/xiaomi/xiaomi.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  xiaomi:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/xiaomi/xiaomi.yaml"
    path: ./ruleset/xiaomi.yaml
    interval: 86400

rules:
  - RULE-SET,xiaomi,PROXY
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