<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/remix/service.svg" alt="Kuaishou 图标" width="72" height="72">

# Kuaishou — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `kuaishou` |
| 类型 | service |
| Provider / 服务集 | `kuaishou` |
| 规则浏览路径 | `kuaishou/kuaishou/kuaishou.yaml` |
| 语义规则数量 | **678** |
| 语义 SHA-256 | `bad70f170bd920997f34bf6ac19e839f2c6a59c3d6ae0142b3c0aed5e4dad68e` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标：**remix semantic fallback**

- Style：`remix`
- Identity：`semantic.fallback.remix`
- 本地 V4 Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/remix/service.svg`
- 语义：仅用于完整覆盖规则服务，不代表官方品牌 Logo。

风格层参考：Lucide / Tabler / Phosphor / Material Symbols / Fluent UI / Heroicons / Remix / Bootstrap / Solar。

## 3. 服务集与层级

所属服务集：[kuaishou](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/kuaishou/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/kuaishou/kuaishou/kuaishou.yaml` | 678 | 13798 | `e50f8f6410801fc368f6a022b3a672fa7a2bb2d1efba3b6a8f3aa31d1fbcd652` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/kuaishou/kuaishou/kuaishou.yaml) |
| loon | `loon/kuaishou/kuaishou/kuaishou.list` | 678 | 19203 | `7d3329c351f2809a71502d5c1cfac48a792c1283d3a9cd9f2309d372b54c8420` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/kuaishou/kuaishou/kuaishou.list) |
| mihomo | `mihomo/kuaishou/kuaishou/kuaishou.yaml` | 678 | 21924 | `9246af48bed0bf4f8c88e9cbfcda4d25c60f4c17ed3ffb89716ff80472dfcf0b` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/kuaishou/kuaishou/kuaishou.yaml) |
| quantumultx | `quantumultx/kuaishou/kuaishou/kuaishou.list` | 678 | 23271 | `5f9e3d6729f2d2ac718243de0c5f5a7789d5330368fe2b99e79ed36d35e10b48` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/kuaishou/kuaishou/kuaishou.list) |
| shadowrocket | `shadowrocket/kuaishou/kuaishou/kuaishou.list` | 678 | 19203 | `7d3329c351f2809a71502d5c1cfac48a792c1283d3a9cd9f2309d372b54c8420` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/kuaishou/kuaishou/kuaishou.list) |
| singbox | `singbox/kuaishou/kuaishou/kuaishou.json` | 0 | 17250 | `ff86f738d93a044cc83d6e5f70ba49264d27b2db13a5f3968e51c4b154c33ce7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/kuaishou/kuaishou/kuaishou.json) |
| surge | `surge/kuaishou/kuaishou/kuaishou.list` | 678 | 19203 | `7d3329c351f2809a71502d5c1cfac48a792c1283d3a9cd9f2309d372b54c8420` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/kuaishou/kuaishou/kuaishou.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/kuaishou/kuaishou/kuaishou.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/kuaishou/kuaishou/kuaishou.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/kuaishou/kuaishou/kuaishou.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/kuaishou/kuaishou/kuaishou.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/kuaishou/kuaishou/kuaishou.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/kuaishou/kuaishou/kuaishou.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/kuaishou/kuaishou/kuaishou.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  kuaishou:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/kuaishou/kuaishou/kuaishou.yaml"
    path: ./ruleset/kuaishou.yaml
    interval: 86400

rules:
  - RULE-SET,kuaishou,PROXY
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