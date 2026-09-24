<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/tabler/service.svg" alt="Xianyu 图标" width="72" height="72">

# Xianyu — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `xianyu` |
| 类型 | service |
| Provider / 服务集 | `alibaba` |
| 规则浏览路径 | `alibaba/xianyu/xianyu.yaml` |
| 语义规则数量 | **16** |
| 语义 SHA-256 | `c68709fa5b84bb4eb5a12dfebcff74576307a92dcc5aa8ca303a92c8e6953da0` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标：**tabler semantic fallback**

- Style：`tabler`
- Identity：`semantic.fallback.tabler`
- 本地 V4 Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/tabler/service.svg`
- 语义：仅用于完整覆盖规则服务，不代表官方品牌 Logo。

风格层参考：Lucide / Tabler / Phosphor / Material Symbols / Fluent UI / Heroicons / Remix / Bootstrap / Solar。

## 3. 服务集与层级

所属服务集：[alibaba](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/alibaba/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/alibaba/xianyu/xianyu.yaml` | 16 | 296 | `2c45b63e7323e7f35eac4e0a6c8f3ef67101b044bfd8083a47d8a637569f342d` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/alibaba/xianyu/xianyu.yaml) |
| loon | `loon/alibaba/xianyu/xianyu.list` | 16 | 405 | `049574f8ba4a0ff11b4dfdd29cd1f3d53626d0d172f36bfc22975b4accb86ba0` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/alibaba/xianyu/xianyu.list) |
| mihomo | `mihomo/alibaba/xianyu/xianyu.yaml` | 16 | 478 | `c7742aad8f0e187239996d2d596e41079e8a98e04d2305161dcfb0567724e0e0` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/alibaba/xianyu/xianyu.yaml) |
| quantumultx | `quantumultx/alibaba/xianyu/xianyu.list` | 16 | 501 | `5ef401b1262eb096e3d895a6dd336dd8c5a38697e548d3026e6981b9fcc477a7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/alibaba/xianyu/xianyu.list) |
| shadowrocket | `shadowrocket/alibaba/xianyu/xianyu.list` | 16 | 405 | `049574f8ba4a0ff11b4dfdd29cd1f3d53626d0d172f36bfc22975b4accb86ba0` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/alibaba/xianyu/xianyu.list) |
| singbox | `singbox/alibaba/xianyu/xianyu.json` | 0 | 438 | `6fe24962ac0fd8df78115d728b2468ca3f976b4d5284d53e1eb2fcf09e597192` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/alibaba/xianyu/xianyu.json) |
| surge | `surge/alibaba/xianyu/xianyu.list` | 16 | 405 | `049574f8ba4a0ff11b4dfdd29cd1f3d53626d0d172f36bfc22975b4accb86ba0` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/alibaba/xianyu/xianyu.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/alibaba/xianyu/xianyu.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/alibaba/xianyu/xianyu.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/alibaba/xianyu/xianyu.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/alibaba/xianyu/xianyu.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/alibaba/xianyu/xianyu.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/alibaba/xianyu/xianyu.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/alibaba/xianyu/xianyu.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  xianyu:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/alibaba/xianyu/xianyu.yaml"
    path: ./ruleset/xianyu.yaml
    interval: 86400

rules:
  - RULE-SET,xianyu,PROXY
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