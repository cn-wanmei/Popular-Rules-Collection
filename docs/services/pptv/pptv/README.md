<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/phosphor/service.svg" alt="PPTV 图标" width="72" height="72">

# PPTV — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `pptv` |
| 类型 | service |
| Provider / 服务集 | `pptv` |
| 规则浏览路径 | `pptv/pptv/pptv.yaml` |
| 语义规则数量 | **19** |
| 语义 SHA-256 | `d1d71c83f19b7ff3ab5ca8d68261e7b59b33edb1fbdeae075b23c0b8b59fb024` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标：**phosphor semantic fallback**

- Style：`phosphor`
- Identity：`semantic.fallback.phosphor`
- 本地 V4 Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/phosphor/service.svg`
- 语义：仅用于完整覆盖规则服务，不代表官方品牌 Logo。

风格层参考：Lucide / Tabler / Phosphor / Material Symbols / Fluent UI / Heroicons / Remix / Bootstrap / Solar。

## 3. 服务集与层级

所属服务集：[pptv](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/pptv/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/pptv/pptv/pptv.yaml` | 19 | 342 | `b83ee04c66f8a783d9849109b757340742677977757603249f4a50ee2ff739aa` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/pptv/pptv/pptv.yaml) |
| loon | `loon/pptv/pptv/pptv.list` | 19 | 475 | `4020aea285ee2b4ff8785b66b2757e2854a7732d148fe31efa94d3e7a09b9f44` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/pptv/pptv/pptv.list) |
| mihomo | `mihomo/pptv/pptv/pptv.yaml` | 19 | 560 | `412a5e7de1f5bbb0f5c8ee831804afa9c43486a07b36e80ff9e8ba43dd9f1747` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/pptv/pptv/pptv.yaml) |
| quantumultx | `quantumultx/pptv/pptv/pptv.list` | 19 | 589 | `bbad6bf9967ec4c6b0ab7501edd3d9d9c9d2e0a161b3d03d7051dd48e9d47953` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/pptv/pptv/pptv.list) |
| shadowrocket | `shadowrocket/pptv/pptv/pptv.list` | 19 | 475 | `4020aea285ee2b4ff8785b66b2757e2854a7732d148fe31efa94d3e7a09b9f44` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/pptv/pptv/pptv.list) |
| singbox | `singbox/pptv/pptv/pptv.json` | 0 | 499 | `bfdfd797cac15ceb0dc85a9038521bd6c3514491cf9a12b24d613458cc140db8` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/pptv/pptv/pptv.json) |
| surge | `surge/pptv/pptv/pptv.list` | 19 | 475 | `4020aea285ee2b4ff8785b66b2757e2854a7732d148fe31efa94d3e7a09b9f44` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/pptv/pptv/pptv.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/pptv/pptv/pptv.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/pptv/pptv/pptv.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/pptv/pptv/pptv.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/pptv/pptv/pptv.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/pptv/pptv/pptv.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/pptv/pptv/pptv.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/pptv/pptv/pptv.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  pptv:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/pptv/pptv/pptv.yaml"
    path: ./ruleset/pptv.yaml
    interval: 86400

rules:
  - RULE-SET,pptv,PROXY
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