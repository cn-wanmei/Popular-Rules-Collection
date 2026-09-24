<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/lucide/service.svg" alt="Battle.net 图标" width="72" height="72">

# Battle.net — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `battlenet` |
| 类型 | service |
| Provider / 服务集 | `blizzard` |
| 规则浏览路径 | `blizzard/battlenet/battlenet.yaml` |
| 语义规则数量 | **62** |
| 语义 SHA-256 | `7a68f906db296f21696efcf6737973c702012f0510dcbe12368e3301e00b1aae` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标：**lucide semantic fallback**

- Style：`lucide`
- Identity：`semantic.fallback.lucide`
- 本地 V4 Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/lucide/service.svg`
- 语义：仅用于完整覆盖规则服务，不代表官方品牌 Logo。

风格层参考：Lucide / Tabler / Phosphor / Material Symbols / Fluent UI / Heroicons / Remix / Bootstrap / Solar。

## 3. 服务集与层级

所属服务集：[blizzard](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/blizzard/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/blizzard/battlenet/battlenet.yaml` | 62 | 1552 | `f271d0b7de9fd6b775a7de07b9d12516a18dc484c225d990d308212b09441d6f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/blizzard/battlenet/battlenet.yaml) |
| loon | `loon/blizzard/battlenet/battlenet.list` | 62 | 1878 | `92375aa2e7eeb6fc69ff0d77ed54d0358116918e94bb284b770ecc0fd1a470cd` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/blizzard/battlenet/battlenet.list) |
| mihomo | `mihomo/blizzard/battlenet/battlenet.yaml` | 62 | 2135 | `acaf8eb5c5ed140abefe0293476c6b20ee698994816dda57641b98c1f8f880a5` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/blizzard/battlenet/battlenet.yaml) |
| quantumultx | `quantumultx/blizzard/battlenet/battlenet.list` | 62 | 2296 | `c8f76cc9bd408d2e172679bd44e18463332eb831beec3b8edf43128316c66a85` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/blizzard/battlenet/battlenet.list) |
| shadowrocket | `shadowrocket/blizzard/battlenet/battlenet.list` | 62 | 1878 | `92375aa2e7eeb6fc69ff0d77ed54d0358116918e94bb284b770ecc0fd1a470cd` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/blizzard/battlenet/battlenet.list) |
| singbox | `singbox/blizzard/battlenet/battlenet.json` | 0 | 1938 | `e311972e672207b233025c7f30aef242c676657b6c126b474984d04a443c693e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/blizzard/battlenet/battlenet.json) |
| surge | `surge/blizzard/battlenet/battlenet.list` | 62 | 1878 | `92375aa2e7eeb6fc69ff0d77ed54d0358116918e94bb284b770ecc0fd1a470cd` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/blizzard/battlenet/battlenet.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/blizzard/battlenet/battlenet.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/blizzard/battlenet/battlenet.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/blizzard/battlenet/battlenet.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/blizzard/battlenet/battlenet.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/blizzard/battlenet/battlenet.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/blizzard/battlenet/battlenet.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/blizzard/battlenet/battlenet.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  battlenet:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/blizzard/battlenet/battlenet.yaml"
    path: ./ruleset/battlenet.yaml
    interval: 86400

rules:
  - RULE-SET,battlenet,PROXY
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