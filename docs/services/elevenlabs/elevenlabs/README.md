<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/fluent/service.svg" alt="ElevenLabs 图标" width="72" height="72">

# ElevenLabs — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `elevenlabs` |
| 类型 | service |
| Provider / 服务集 | `elevenlabs` |
| 规则浏览路径 | `elevenlabs/elevenlabs/elevenlabs.yaml` |
| 语义规则数量 | **2** |
| 语义 SHA-256 | `c7f48548a2b07593718f8ecc1ab52eaa8e1ac519b0a005a80c8793541544d47d` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标：**fluent semantic fallback**

- Style：`fluent`
- Identity：`semantic.fallback.fluent`
- 本地 V4 Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/fluent/service.svg`
- 语义：仅用于完整覆盖规则服务，不代表官方品牌 Logo。

风格层参考：Lucide / Tabler / Phosphor / Material Symbols / Fluent UI / Heroicons / Remix / Bootstrap / Solar。

## 3. 服务集与层级

所属服务集：[elevenlabs](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/elevenlabs/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/elevenlabs/elevenlabs/elevenlabs.yaml` | 4 | 101 | `d4d299033b7236c8df2278cb8b01223902bc3de03ecb74305bde645635c38da6` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/elevenlabs/elevenlabs/elevenlabs.yaml) |
| loon | `loon/elevenlabs/elevenlabs/elevenlabs.list` | 4 | 114 | `5a6d0cb85a39ce8a9f4df7cad21f76a8af74769fce6b98a9ed2e1345a5409f1d` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/elevenlabs/elevenlabs/elevenlabs.list) |
| mihomo | `mihomo/elevenlabs/elevenlabs/elevenlabs.yaml` | 4 | 139 | `bfa1e402851e01614e19e1ca4e0c548febf2982c31da96675ad96b05c47a4813` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/elevenlabs/elevenlabs/elevenlabs.yaml) |
| quantumultx | `quantumultx/elevenlabs/elevenlabs/elevenlabs.list` | 4 | 138 | `b1299a3f8d4573284006d6112d0b988a481e4d810b61065f7cc513529a3232d6` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/elevenlabs/elevenlabs/elevenlabs.list) |
| shadowrocket | `shadowrocket/elevenlabs/elevenlabs/elevenlabs.list` | 4 | 114 | `5a6d0cb85a39ce8a9f4df7cad21f76a8af74769fce6b98a9ed2e1345a5409f1d` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/elevenlabs/elevenlabs/elevenlabs.list) |
| singbox | `singbox/elevenlabs/elevenlabs/elevenlabs.json` | 0 | 183 | `b24919754e18230a5b9ac298d0e6af7f9d1c6867cef85ad1e5de2ab9f10a279a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/elevenlabs/elevenlabs/elevenlabs.json) |
| surge | `surge/elevenlabs/elevenlabs/elevenlabs.list` | 4 | 114 | `5a6d0cb85a39ce8a9f4df7cad21f76a8af74769fce6b98a9ed2e1345a5409f1d` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/elevenlabs/elevenlabs/elevenlabs.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/elevenlabs/elevenlabs/elevenlabs.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/elevenlabs/elevenlabs/elevenlabs.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/elevenlabs/elevenlabs/elevenlabs.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/elevenlabs/elevenlabs/elevenlabs.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/elevenlabs/elevenlabs/elevenlabs.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/elevenlabs/elevenlabs/elevenlabs.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/elevenlabs/elevenlabs/elevenlabs.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  elevenlabs:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/elevenlabs/elevenlabs/elevenlabs.yaml"
    path: ./ruleset/elevenlabs.yaml
    interval: 86400

rules:
  - RULE-SET,elevenlabs,PROXY
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