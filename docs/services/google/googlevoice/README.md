<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/fluent/service.svg" alt="Google Voice 图标" width="72" height="72">

# Google Voice — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `googlevoice` |
| 类型 | service |
| Provider / 服务集 | `google` |
| 规则浏览路径 | `google/googlevoice/googlevoice.yaml` |
| 语义规则数量 | **1** |
| 语义 SHA-256 | `555b8533d71f542bb779effaea2f8e7f341e62744a37061173e295202c528a52` |
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

所属服务集：[google](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/google/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/google/googlevoice/googlevoice.yaml` | 1 | 36 | `e18c9777c637cb12324cb508e87bb39bc6dfc2f715b486de7be57834490552fe` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/google/googlevoice/googlevoice.yaml) |
| loon | `loon/google/googlevoice/googlevoice.list` | 1 | 25 | `71aee9dfa0771f5d327d29bf9e0f1132c0819c5faa05ff3fe561f6987ee5a3c8` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/google/googlevoice/googlevoice.list) |
| mihomo | `mihomo/google/googlevoice/googlevoice.yaml` | 1 | 38 | `2336a3dc9d21717dc634e1523820a1c0daddc409225e195b82035d64c111c8ee` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/google/googlevoice/googlevoice.yaml) |
| quantumultx | `quantumultx/google/googlevoice/googlevoice.list` | 1 | 31 | `e5f4b7491a549842fc187e66badbf5d2d6a00256a6329177cb5b6a1a919028ae` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/google/googlevoice/googlevoice.list) |
| shadowrocket | `shadowrocket/google/googlevoice/googlevoice.list` | 1 | 25 | `71aee9dfa0771f5d327d29bf9e0f1132c0819c5faa05ff3fe561f6987ee5a3c8` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/google/googlevoice/googlevoice.list) |
| singbox | `singbox/google/googlevoice/googlevoice.json` | 0 | 103 | `9657318ec70a746221abd96b12daf6d006a4e9e0624d064e115d51ec29fd20de` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/google/googlevoice/googlevoice.json) |
| surge | `surge/google/googlevoice/googlevoice.list` | 1 | 25 | `71aee9dfa0771f5d327d29bf9e0f1132c0819c5faa05ff3fe561f6987ee5a3c8` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/google/googlevoice/googlevoice.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/google/googlevoice/googlevoice.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/google/googlevoice/googlevoice.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/google/googlevoice/googlevoice.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/google/googlevoice/googlevoice.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/google/googlevoice/googlevoice.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/google/googlevoice/googlevoice.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/google/googlevoice/googlevoice.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  googlevoice:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/google/googlevoice/googlevoice.yaml"
    path: ./ruleset/googlevoice.yaml
    interval: 86400

rules:
  - RULE-SET,googlevoice,PROXY
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