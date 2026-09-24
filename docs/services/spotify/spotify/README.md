<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/spotify.png" alt="Spotify 图标" width="72" height="72">

# Spotify — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `spotify` |
| 类型 | service |
| Provider / 服务集 | `spotify` |
| 规则浏览路径 | `spotify/spotify/spotify.yaml` |
| 语义规则数量 | **38** |
| 语义 SHA-256 | `0eee92f7e3b61de22168a5bd03bc4eabb653b965adaf01ef2bdd8063ac765b0d` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标：**Official / Brand Native**

- Identity：`brand.spotify`
- 来源：Current V3 已发布品牌身份资产
- Icon Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/spotify.png`
- Digest：`60dce5d4c7d10c196d83dc40fc3db745a7cdf3a515cbf5ad6a0c49dfe37fb3e0`

本服务存在可信品牌身份，因此 V4 不使用九风格 fallback 重绘该品牌 Logo。

风格层参考：Lucide / Tabler / Phosphor / Material Symbols / Fluent UI / Heroicons / Remix / Bootstrap / Solar。

## 3. 服务集与层级

所属服务集：[spotify](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/spotify/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/spotify/spotify/spotify.yaml` | 62 | 1657 | `1617ff56edd32bc606023780c4a02e755b417abad3c60d91a03278ecce239db4` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/spotify/spotify/spotify.yaml) |
| loon | `loon/spotify/spotify/spotify.list` | 62 | 1960 | `e51a09bbaa4d0d9f584c9834b25e8e5344c4a3414ab184aedcdd3dafb5f29e21` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/spotify/spotify/spotify.list) |
| mihomo | `mihomo/spotify/spotify/spotify.yaml` | 62 | 2217 | `c845951d596152f5a54c4d4ec62b95083930be840de630d86208f889f755415b` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/spotify/spotify/spotify.yaml) |
| quantumultx | `quantumultx/spotify/spotify/spotify.list` | 62 | 2336 | `4162c7a044659cfac69655ced21a75de2cea81bea10785d7e7c1a1717b28f3b9` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/spotify/spotify/spotify.list) |
| shadowrocket | `shadowrocket/spotify/spotify/spotify.list` | 62 | 1960 | `e51a09bbaa4d0d9f584c9834b25e8e5344c4a3414ab184aedcdd3dafb5f29e21` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/spotify/spotify/spotify.list) |
| singbox | `singbox/spotify/spotify/spotify.json` | 0 | 2071 | `edab95120d42d8d1df52eedacfb3e57b3694593a2b90c66cdae08c898b9ae23f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/spotify/spotify/spotify.json) |
| surge | `surge/spotify/spotify/spotify.list` | 62 | 1960 | `e51a09bbaa4d0d9f584c9834b25e8e5344c4a3414ab184aedcdd3dafb5f29e21` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/spotify/spotify/spotify.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/spotify/spotify/spotify.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/spotify/spotify/spotify.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/spotify/spotify/spotify.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/spotify/spotify/spotify.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/spotify/spotify/spotify.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/spotify/spotify/spotify.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/spotify/spotify/spotify.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  spotify:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/spotify/spotify/spotify.yaml"
    path: ./ruleset/spotify.yaml
    interval: 86400

rules:
  - RULE-SET,spotify,PROXY
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