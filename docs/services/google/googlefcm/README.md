<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/heroicons/service.svg" alt="Google FCM 图标" width="72" height="72">

# Google FCM — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `googlefcm` |
| 类型 | service |
| Provider / 服务集 | `google` |
| 规则浏览路径 | `google/googlefcm/googlefcm.yaml` |
| 语义规则数量 | **13** |
| 语义 SHA-256 | `1e3d116a03f64650b9cc4b7803cf5c565e642003df11518f8fadf27a7255a0b4` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标：**heroicons semantic fallback**

- Style：`heroicons`
- Identity：`semantic.fallback.heroicons`
- 本地 V4 Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/heroicons/service.svg`
- 语义：仅用于完整覆盖规则服务，不代表官方品牌 Logo。

风格层参考：Lucide / Tabler / Phosphor / Material Symbols / Fluent UI / Heroicons / Remix / Bootstrap / Solar。

## 3. 服务集与层级

所属服务集：[google](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/google/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/google/googlefcm/googlefcm.yaml` | 13 | 378 | `7d9ce3304df0ddcead7d1500cecc736d711ff0436e7bbf42805e2eafb0ab83a4` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/google/googlefcm/googlefcm.yaml) |
| loon | `loon/google/googlefcm/googlefcm.list` | 13 | 463 | `d5416f51714c2a6e111c090136eaf04f90a352fdb549125dfefd63fa89259c85` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/google/googlefcm/googlefcm.list) |
| mihomo | `mihomo/google/googlefcm/googlefcm.yaml` | 13 | 524 | `f4adc194c1a8fd435cedecc165ad44745e869c22b5413233c46cb6db44fd2bbc` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/google/googlefcm/googlefcm.yaml) |
| quantumultx | `quantumultx/google/googlefcm/googlefcm.list` | 13 | 541 | `ce563c7fdabf600c1031bfcbecd471a4fe9eb0ccf8b8cfe6ca91f0da49ec4a2c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/google/googlefcm/googlefcm.list) |
| shadowrocket | `shadowrocket/google/googlefcm/googlefcm.list` | 13 | 463 | `d5416f51714c2a6e111c090136eaf04f90a352fdb549125dfefd63fa89259c85` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/google/googlefcm/googlefcm.list) |
| singbox | `singbox/google/googlefcm/googlefcm.json` | 0 | 505 | `44b2ab01b2f1e2b5b9d2870fdcbd74a950b3846910fc1b5198f13f384d953422` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/google/googlefcm/googlefcm.json) |
| surge | `surge/google/googlefcm/googlefcm.list` | 13 | 463 | `d5416f51714c2a6e111c090136eaf04f90a352fdb549125dfefd63fa89259c85` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/google/googlefcm/googlefcm.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/google/googlefcm/googlefcm.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/google/googlefcm/googlefcm.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/google/googlefcm/googlefcm.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/google/googlefcm/googlefcm.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/google/googlefcm/googlefcm.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/google/googlefcm/googlefcm.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/google/googlefcm/googlefcm.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  googlefcm:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/google/googlefcm/googlefcm.yaml"
    path: ./ruleset/googlefcm.yaml
    interval: 86400

rules:
  - RULE-SET,googlefcm,PROXY
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