<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/gitlab.png" alt="GitLab 图标" width="72" height="72">

# GitLab — 分流规则说明

> 当前服务页由 Rule Index、Generated Manifest 与 Icon Library V4 共同驱动。品牌身份优先；无可信品牌身份时使用本地 semantic fallback。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| Service ID | `gitlab` |
| 类型 | service |
| Provider / 服务集 | `gitlab` |
| 规则浏览路径 | `gitlab/gitlab/gitlab.yaml` |
| 语义规则数量 | **6** |
| 语义 SHA-256 | `7aabf5b1c8504069effd9df0869e8653366a482d462b1c1631ff9ab2be577b38` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标：**Official / Brand Native**

- Identity：`brand.gitlab`
- 来源：Current V3 已发布品牌身份资产
- Icon Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/gitlab.png`
- Digest：`227eac3506058b9663b4e38fdfceeeadf3f9d7893c3b3a5eb652fce84a780b4b`

本服务存在可信品牌身份，因此 V4 不使用九风格 fallback 重绘该品牌 Logo。

风格层参考：Lucide / Tabler / Phosphor / Material Symbols / Fluent UI / Heroicons / Remix / Bootstrap / Solar。

## 3. 服务集与层级

所属服务集：[gitlab](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/gitlab/README.md)

当前层级由 `rule/_index.yaml` 的物理路径决定，不根据品牌名称猜测父子关系。

## 4. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/gitlab/gitlab/gitlab.yaml` | 6 | 166 | `2fba09cb71581377c4e72a523316dc47796965bdce7b0a22b0609277eb4966e0` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/gitlab/gitlab/gitlab.yaml) |
| loon | `loon/gitlab/gitlab/gitlab.list` | 6 | 195 | `dbb0cdeda8d7617e463e8306e4f35fb32d3a76230d5c26d045b2337f0ddf9d79` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/gitlab/gitlab/gitlab.list) |
| mihomo | `mihomo/gitlab/gitlab/gitlab.yaml` | 6 | 228 | `f5015bf01b52d6f985e6902331a5e582a42dcf492d7013b9632fd150bbba2465` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/gitlab/gitlab/gitlab.yaml) |
| quantumultx | `quantumultx/gitlab/gitlab/gitlab.list` | 6 | 231 | `075ab84d3f10581be98b51f448b72a43b81af0e19930ed33320aa34185370b76` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/gitlab/gitlab/gitlab.list) |
| shadowrocket | `shadowrocket/gitlab/gitlab/gitlab.list` | 6 | 195 | `dbb0cdeda8d7617e463e8306e4f35fb32d3a76230d5c26d045b2337f0ddf9d79` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/gitlab/gitlab/gitlab.list) |
| singbox | `singbox/gitlab/gitlab/gitlab.json` | 0 | 258 | `0fb611f54aa0cba33aa42525e0ca6d190e85d6df9ccb2f487808b8e3009191e2` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/gitlab/gitlab/gitlab.json) |
| surge | `surge/gitlab/gitlab/gitlab.list` | 6 | 195 | `dbb0cdeda8d7617e463e8306e4f35fb32d3a76230d5c26d045b2337f0ddf9d79` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/gitlab/gitlab/gitlab.list) |

### 4.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/gitlab/gitlab/gitlab.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/gitlab/gitlab/gitlab.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/gitlab/gitlab/gitlab.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/gitlab/gitlab/gitlab.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/gitlab/gitlab/gitlab.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/gitlab/gitlab/gitlab.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/gitlab/gitlab/gitlab.list`

## 5. 使用方法

选择客户端 → 复制对应 Raw → 加入远程 Rule Set / Rule Provider / rule-set → 绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用其他目录的 YAML、JSON、LIST；`rule/` 不是客户端运行时输入。

### 5.1 Mihomo 结构示例

```yaml
rule-providers:
  gitlab:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/gitlab/gitlab/gitlab.yaml"
    path: ./ruleset/gitlab.yaml
    interval: 86400

rules:
  - RULE-SET,gitlab,PROXY
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