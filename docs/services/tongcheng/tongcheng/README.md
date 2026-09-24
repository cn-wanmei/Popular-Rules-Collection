<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/material-symbols/service.svg" alt="Tongcheng 图标" width="72" height="72">

# Tongcheng — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `tongcheng` |
| 类型 | service |
| Provider / 服务集 | `tongcheng` |
| 规则浏览路径 | `tongcheng/tongcheng/tongcheng.yaml` |
| 语义规则数量 | **8** |
| 语义 SHA-256 | `749b869a6b427f4203f36811b178c039dbcac81c5333e98f312ca54ddb1b2eab` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标：**material-symbols semantic fallback**

- Style：`material-symbols`
- Identity：`semantic.fallback.material-symbols`
- 本地 V4 Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/material-symbols/service.svg`
- 语义：仅用于完整覆盖规则服务，不代表官方品牌 Logo。

风格层参考：Lucide / Tabler / Phosphor / Material Symbols / Fluent UI / Heroicons / Remix / Bootstrap / Solar。

## 3. 服务集与层级

所属服务集：[tongcheng](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/tongcheng/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/tongcheng/tongcheng/tongcheng.yaml` | 8 | 148 | `f95018071b3d1995b926d2dd677737c492dc6e64c68140c8dfe218f034a4500a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/tongcheng/tongcheng/tongcheng.yaml) |
| loon | `loon/tongcheng/tongcheng/tongcheng.list` | 8 | 193 | `e2b14cabe70fe1971a1485fcd5dce3a062d228e80b2c4209be4a3ddcf65f43f0` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/tongcheng/tongcheng/tongcheng.list) |
| mihomo | `mihomo/tongcheng/tongcheng/tongcheng.yaml` | 8 | 234 | `154baae7e704104d55475d652095e0c9a2086901986b183fc9668186bd4d994f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/tongcheng/tongcheng/tongcheng.yaml) |
| quantumultx | `quantumultx/tongcheng/tongcheng/tongcheng.list` | 8 | 241 | `2862546cd84fee4460a717caf02c8d6a8ed9ba7c66bcbdaeb69488c649b147fc` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/tongcheng/tongcheng/tongcheng.list) |
| shadowrocket | `shadowrocket/tongcheng/tongcheng/tongcheng.list` | 8 | 193 | `e2b14cabe70fe1971a1485fcd5dce3a062d228e80b2c4209be4a3ddcf65f43f0` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/tongcheng/tongcheng/tongcheng.list) |
| singbox | `singbox/tongcheng/tongcheng/tongcheng.json` | 0 | 250 | `6953092aadf830555c2ed9acc432ac36ae55b6fb7731b5e21c380db0aa685bf9` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/tongcheng/tongcheng/tongcheng.json) |
| surge | `surge/tongcheng/tongcheng/tongcheng.list` | 8 | 193 | `e2b14cabe70fe1971a1485fcd5dce3a062d228e80b2c4209be4a3ddcf65f43f0` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/tongcheng/tongcheng/tongcheng.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/tongcheng/tongcheng/tongcheng.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/tongcheng/tongcheng/tongcheng.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/tongcheng/tongcheng/tongcheng.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/tongcheng/tongcheng/tongcheng.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/tongcheng/tongcheng/tongcheng.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/tongcheng/tongcheng/tongcheng.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/tongcheng/tongcheng/tongcheng.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  tongcheng:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/tongcheng/tongcheng/tongcheng.yaml"
    path: ./ruleset/tongcheng.yaml
    interval: 86400

rules:
  - RULE-SET,tongcheng,PROXY
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