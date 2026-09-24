<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/rockstar.png" alt="Rockstar Games 图标" width="72" height="72">

# Rockstar Games — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `rockstar` |
| 类型 | service |
| Provider / 服务集 | `rockstar` |
| 规则浏览路径 | `rockstar/rockstar/rockstar.yaml` |
| 语义规则数量 | **5** |
| 语义 SHA-256 | `708070e42915e30662bf6ed5cb1db12dc67df8dc842af96d881063aa66d4398a` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标：**Official / Brand Native**

- Identity：`brand.rockstar`
- 来源：Current V3 已发布品牌身份资产
- Icon Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/rockstar.png`
- Digest：`e612da538c5cac08c892c16ff69baf78a7782c38377fad0cc89a181f3edf8dc5`

本服务存在可信品牌身份，因此 V4 不使用九风格 fallback 重绘该品牌 Logo。

风格层参考：Lucide / Tabler / Phosphor / Material Symbols / Fluent UI / Heroicons / Remix / Bootstrap / Solar。

## 3. 服务集与层级

所属服务集：[rockstar](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/rockstar/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/rockstar/rockstar/rockstar.yaml` | 5 | 197 | `50b7adfefb8a3126cc1c81d52d72550749855da64e42569336cbd979d5c0d4d7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/rockstar/rockstar/rockstar.yaml) |
| loon | `loon/rockstar/rockstar/rockstar.list` | 5 | 218 | `eaed1e732a3df831d9adec608c1104dc3045e323a100b01b848ee6c0233f4a55` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/rockstar/rockstar/rockstar.list) |
| mihomo | `mihomo/rockstar/rockstar/rockstar.yaml` | 5 | 247 | `65b2f9464815f9127eb89ba83fce914109efbf0fe64deca25b065fb6a4c7cb60` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/rockstar/rockstar/rockstar.yaml) |
| quantumultx | `quantumultx/rockstar/rockstar/rockstar.list` | 5 | 248 | `288376f16c1d6b7d918548dd1a1859af7b19697e7004a9057aaa32d1900ae9b1` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/rockstar/rockstar/rockstar.list) |
| shadowrocket | `shadowrocket/rockstar/rockstar/rockstar.list` | 5 | 218 | `eaed1e732a3df831d9adec608c1104dc3045e323a100b01b848ee6c0233f4a55` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/rockstar/rockstar/rockstar.list) |
| singbox | `singbox/rockstar/rockstar/rockstar.json` | 0 | 284 | `adad07b3c6568dfabf4dcfb956387ae82f560fe66cbbf8be75db3e84859224e2` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/rockstar/rockstar/rockstar.json) |
| surge | `surge/rockstar/rockstar/rockstar.list` | 5 | 218 | `eaed1e732a3df831d9adec608c1104dc3045e323a100b01b848ee6c0233f4a55` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/rockstar/rockstar/rockstar.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/rockstar/rockstar/rockstar.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/rockstar/rockstar/rockstar.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/rockstar/rockstar/rockstar.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/rockstar/rockstar/rockstar.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/rockstar/rockstar/rockstar.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/rockstar/rockstar/rockstar.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/rockstar/rockstar/rockstar.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  rockstar:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/rockstar/rockstar/rockstar.yaml"
    path: ./ruleset/rockstar.yaml
    interval: 86400

rules:
  - RULE-SET,rockstar,PROXY
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