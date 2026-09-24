<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/reddit.png" alt="Reddit 图标" width="72" height="72">

# Reddit — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `reddit` |
| 类型 | service |
| Provider / 服务集 | `reddit` |
| 规则浏览路径 | `reddit/reddit/reddit.yaml` |
| 语义规则数量 | **15** |
| 语义 SHA-256 | `866a91d1f8af211fad9845a1ae9dd1945bbcd96a7cb3c0eb7fe04de4bfec1310` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标：**Official / Brand Native**

- Identity：`brand.reddit`
- 来源：Current V3 已发布品牌身份资产
- Icon Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/reddit.png`
- Digest：`876c22dbaaff9fdc20c974ea0c65248efa49872ff1735b4feed18d38343a23bf`

本服务存在可信品牌身份，因此 V4 不使用九风格 fallback 重绘该品牌 Logo。

风格层参考：Lucide / Tabler / Phosphor / Material Symbols / Fluent UI / Heroicons / Remix / Bootstrap / Solar。

## 3. 服务集与层级

所属服务集：[reddit](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/reddit/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/reddit/reddit/reddit.yaml` | 32 | 734 | `62055abae0085fae4ecbe0e41f8358c5a5e41da15f08812232d66d0b5177df7e` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/reddit/reddit/reddit.yaml) |
| loon | `loon/reddit/reddit/reddit.list` | 32 | 971 | `065fdf7d15bd5ef44f42e9d2dc370df4d6489224e2c7ac2e85c2f870ad896a12` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/reddit/reddit/reddit.list) |
| mihomo | `mihomo/reddit/reddit/reddit.yaml` | 32 | 1108 | `16bc045e2bec1c133502884e3b975adc9a12134c58095726b8359dfc16250e4b` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/reddit/reddit/reddit.yaml) |
| quantumultx | `quantumultx/reddit/reddit/reddit.list` | 32 | 1163 | `658f292722c5e637aa879914420e33d38b5004ceba2cc263eb22a8fabcc2a945` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/reddit/reddit/reddit.list) |
| shadowrocket | `shadowrocket/reddit/reddit/reddit.list` | 32 | 971 | `065fdf7d15bd5ef44f42e9d2dc370df4d6489224e2c7ac2e85c2f870ad896a12` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/reddit/reddit/reddit.list) |
| singbox | `singbox/reddit/reddit/reddit.json` | 0 | 956 | `aba67c1ad1d9e53ca1786db82e7cec8eb42b42e4f395837e4302cd9f1c14b448` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/reddit/reddit/reddit.json) |
| surge | `surge/reddit/reddit/reddit.list` | 32 | 971 | `065fdf7d15bd5ef44f42e9d2dc370df4d6489224e2c7ac2e85c2f870ad896a12` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/reddit/reddit/reddit.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/reddit/reddit/reddit.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/reddit/reddit/reddit.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/reddit/reddit/reddit.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/reddit/reddit/reddit.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/reddit/reddit/reddit.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/reddit/reddit/reddit.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/reddit/reddit/reddit.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  reddit:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/reddit/reddit/reddit.yaml"
    path: ./ruleset/reddit.yaml
    interval: 86400

rules:
  - RULE-SET,reddit,PROXY
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