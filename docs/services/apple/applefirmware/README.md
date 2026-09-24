<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/solar/service.svg" alt="Apple Firmware 图标" width="72" height="72">

# Apple Firmware — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `applefirmware` |
| 类型 | service |
| Provider / 服务集 | `apple` |
| 规则浏览路径 | `apple/applefirmware/applefirmware.yaml` |
| 语义规则数量 | **175** |
| 语义 SHA-256 | `f9dbc0f1a8acb3acd90e7c679745788c5a5930779f02242ece1a304600ab13d4` |
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

所属服务集：[apple](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/apple/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/apple/applefirmware/applefirmware.yaml` | 174 | 3844 | `53f678d2a2996668e42bf1e3b9c440f11964830fb068f01a1ada812b74a5074c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/apple/applefirmware/applefirmware.yaml) |
| loon | `loon/apple/applefirmware/applefirmware.list` | 174 | 5217 | `423b3788b7b4addf8e959a692d149bb28d063725924540d3145c1ff0f3ff4b91` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/apple/applefirmware/applefirmware.list) |
| mihomo | `mihomo/apple/applefirmware/applefirmware.yaml` | 174 | 5922 | `6dd157cdc2aa200450c49f4498357a8804b22266b5ad6fc8203475466bfabe0c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/apple/applefirmware/applefirmware.yaml) |
| quantumultx | `quantumultx/apple/applefirmware/applefirmware.list` | 174 | 6261 | `ffbbd48c3459b566052e26fc84bb543f711c96d1b81ef0740fffe879044241a3` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/apple/applefirmware/applefirmware.list) |
| shadowrocket | `shadowrocket/apple/applefirmware/applefirmware.list` | 174 | 5217 | `423b3788b7b4addf8e959a692d149bb28d063725924540d3145c1ff0f3ff4b91` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/apple/applefirmware/applefirmware.list) |
| singbox | `singbox/apple/applefirmware/applefirmware.json` | 0 | 4776 | `4ce9873eca7c6aa897f49c888f8267e3a36a8c8656539812b7da233b7b0d8775` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/apple/applefirmware/applefirmware.json) |
| surge | `surge/apple/applefirmware/applefirmware.list` | 174 | 5217 | `423b3788b7b4addf8e959a692d149bb28d063725924540d3145c1ff0f3ff4b91` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/apple/applefirmware/applefirmware.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/apple/applefirmware/applefirmware.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/apple/applefirmware/applefirmware.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/apple/applefirmware/applefirmware.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/apple/applefirmware/applefirmware.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/apple/applefirmware/applefirmware.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/apple/applefirmware/applefirmware.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/apple/applefirmware/applefirmware.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  applefirmware:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/apple/applefirmware/applefirmware.yaml"
    path: ./ruleset/applefirmware.yaml
    interval: 86400

rules:
  - RULE-SET,applefirmware,PROXY
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