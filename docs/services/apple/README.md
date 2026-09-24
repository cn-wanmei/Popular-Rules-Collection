<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/apple.png" alt="Apple 图标" width="72" height="72">

# Apple — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `apple` |
| 类型 | provider_aggregate |
| Provider / 服务集 | `apple` |
| 规则浏览路径 | `apple/apple.yaml` |
| 语义规则数量 | **2027** |
| 语义 SHA-256 | `102f86011902e2ea9b7b77bca54fc3b7ac30467c451d68c6dbf773b947680dcf` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标：**Official / Brand Native**

- Identity：`brand.apple`
- 来源：Current V3 已发布品牌身份资产
- Icon Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/apple.png`
- Digest：`2be4f77df5e8f4b6486da4ce9fff209a8e7888f065d0f4e1812c24fcefee707a`

本服务存在可信品牌身份，因此 V4 不使用九风格 fallback 重绘该品牌 Logo。

风格层参考：Lucide / Tabler / Phosphor / Material Symbols / Fluent UI / Heroicons / Remix / Bootstrap / Solar。

## 3. 服务集与层级

所属服务集：[apple](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/apple/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/apple/apple.yaml` | 2014 | 51088 | `8ae3a18902d2c3325b1e72cb7755e8ae2e27fc2bfaf8d41151eda28dc26be42a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/apple/apple.yaml) |
| loon | `loon/apple/apple.list` | 2014 | 65837 | `2797a21bd5710008955fc74051883a8a3d39cdaf4c0c161cbe702db394150088` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/apple/apple.list) |
| mihomo | `mihomo/apple/apple.yaml` | 2014 | 73902 | `10381458e8e9a8f0bddea48f5cbe181bdeda4674908241133f103681b4ff55c0` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/apple/apple.yaml) |
| quantumultx | `quantumultx/apple/apple.list` | 2014 | 77947 | `5b37a5087e122749d052bf09ff6fc8740be182024db8c673e97a8cbdca74963d` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/apple/apple.list) |
| shadowrocket | `shadowrocket/apple/apple.list` | 2014 | 65837 | `2797a21bd5710008955fc74051883a8a3d39cdaf4c0c161cbe702db394150088` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/apple/apple.list) |
| singbox | `singbox/apple/apple.json` | 0 | 61248 | `4edec38d1478f2fc6563e5429322cace081909f21526df22f98df5a1dfc47666` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/apple/apple.json) |
| surge | `surge/apple/apple.list` | 2014 | 65837 | `2797a21bd5710008955fc74051883a8a3d39cdaf4c0c161cbe702db394150088` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/apple/apple.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/apple/apple.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/apple/apple.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/apple/apple.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/apple/apple.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/apple/apple.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/apple/apple.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/apple/apple.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  apple:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/apple/apple.yaml"
    path: ./ruleset/apple.yaml
    interval: 86400

rules:
  - RULE-SET,apple,PROXY
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