<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/pinterest.png" alt="Pinterest 图标" width="72" height="72">

# Pinterest — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `pinterest` |
| 类型 | service |
| Provider / 服务集 | `pinterest` |
| 规则浏览路径 | `pinterest/pinterest/pinterest.yaml` |
| 语义规则数量 | **23** |
| 语义 SHA-256 | `60304acad80f1ebd01f33853978ccd843396c54d42155f66dcd6ee6fb1afa765` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标：**Official / Brand Native**

- Identity：`brand.pinterest`
- 来源：Current V3 已发布品牌身份资产
- Icon Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/pinterest.png`
- Digest：`9e7836c6e12e82eaaed48c8fe504ff79f508497b8aab05e825675172ddfffcc8`

本服务存在可信品牌身份，因此 V4 不使用九风格 fallback 重绘该品牌 Logo。

风格层参考：Lucide / Tabler / Phosphor / Material Symbols / Fluent UI / Heroicons / Remix / Bootstrap / Solar。

## 3. 服务集与层级

所属服务集：[pinterest](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/pinterest/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/pinterest/pinterest/pinterest.yaml` | 23 | 469 | `0c44e9efcc08d9ac7e53c528b80faf6a29b6aac8bfcfaf6dd4cb2b8e9f19c757` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/pinterest/pinterest/pinterest.yaml) |
| loon | `loon/pinterest/pinterest/pinterest.list` | 23 | 634 | `69f544f34f1ad0437c3716b94cd14ee07a4d867986b226bc07f3663d6ebcf448` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/pinterest/pinterest/pinterest.list) |
| mihomo | `mihomo/pinterest/pinterest/pinterest.yaml` | 23 | 735 | `518026a0614bfcd664951a839d91c151c72eae29de2a6cdca0eb316faa7b8021` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/pinterest/pinterest/pinterest.yaml) |
| quantumultx | `quantumultx/pinterest/pinterest/pinterest.list` | 23 | 772 | `3c821a0007e650d59488f67f051d72c85a8c1d4dbc2129bed925dd1088d01f58` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/pinterest/pinterest/pinterest.list) |
| shadowrocket | `shadowrocket/pinterest/pinterest/pinterest.list` | 23 | 634 | `69f544f34f1ad0437c3716b94cd14ee07a4d867986b226bc07f3663d6ebcf448` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/pinterest/pinterest/pinterest.list) |
| singbox | `singbox/pinterest/pinterest/pinterest.json` | 0 | 646 | `86fe8745c803845b9b77ca0a7bcc2b812c5acb18cc3275cd5f86a4040aedcae3` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/pinterest/pinterest/pinterest.json) |
| surge | `surge/pinterest/pinterest/pinterest.list` | 23 | 634 | `69f544f34f1ad0437c3716b94cd14ee07a4d867986b226bc07f3663d6ebcf448` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/pinterest/pinterest/pinterest.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/pinterest/pinterest/pinterest.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/pinterest/pinterest/pinterest.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/pinterest/pinterest/pinterest.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/pinterest/pinterest/pinterest.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/pinterest/pinterest/pinterest.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/pinterest/pinterest/pinterest.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/pinterest/pinterest/pinterest.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  pinterest:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/pinterest/pinterest/pinterest.yaml"
    path: ./ruleset/pinterest.yaml
    interval: 86400

rules:
  - RULE-SET,pinterest,PROXY
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