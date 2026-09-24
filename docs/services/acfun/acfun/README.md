<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/remix/service.svg" alt="AcFun 图标" width="72" height="72">

# AcFun — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `acfun` |
| 类型 | service |
| Provider / 服务集 | `acfun` |
| 规则浏览路径 | `acfun/acfun/acfun.yaml` |
| 语义规则数量 | **10** |
| 语义 SHA-256 | `04edec7e594b788dab5180df4e5b785d8be9c204023cb138a30c7a9b18e19cab` |
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

所属服务集：[acfun](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/acfun/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/acfun/acfun/acfun.yaml` | 12 | 233 | `7ec172c4221243f36ac3c619e390f18d0399ad4a797d91aee53b1ab77e265a18` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/acfun/acfun/acfun.yaml) |
| loon | `loon/acfun/acfun/acfun.list` | 12 | 310 | `09a147ebdddfb1b37e5003e2246d0193395d05822439da172bcea2420671ec3c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/acfun/acfun/acfun.list) |
| mihomo | `mihomo/acfun/acfun/acfun.yaml` | 12 | 367 | `4fbcde6ca3cbe95674c5dd198568942e20c61dafae942ba5098fa4f31dab8758` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/acfun/acfun/acfun.yaml) |
| quantumultx | `quantumultx/acfun/acfun/acfun.list` | 12 | 382 | `c0b41ad29005f42dfdaec1403febb2d91e9b719aadd327df1a1c7452e9139508` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/acfun/acfun/acfun.list) |
| shadowrocket | `shadowrocket/acfun/acfun/acfun.list` | 12 | 310 | `09a147ebdddfb1b37e5003e2246d0193395d05822439da172bcea2420671ec3c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/acfun/acfun/acfun.list) |
| singbox | `singbox/acfun/acfun/acfun.json` | 0 | 355 | `78700eef35b09c190e627dba17af54f92e9db2f22b777d01cf1ef78ec3aa8923` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/acfun/acfun/acfun.json) |
| surge | `surge/acfun/acfun/acfun.list` | 12 | 310 | `09a147ebdddfb1b37e5003e2246d0193395d05822439da172bcea2420671ec3c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/acfun/acfun/acfun.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/acfun/acfun/acfun.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/acfun/acfun/acfun.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/acfun/acfun/acfun.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/acfun/acfun/acfun.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/acfun/acfun/acfun.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/acfun/acfun/acfun.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/acfun/acfun/acfun.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  acfun:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/acfun/acfun/acfun.yaml"
    path: ./ruleset/acfun.yaml
    interval: 86400

rules:
  - RULE-SET,acfun,PROXY
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