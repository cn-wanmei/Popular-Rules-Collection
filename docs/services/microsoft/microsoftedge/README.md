<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/placeholder.png" alt="Microsoft Edge 图标" width="72" height="72">

# Microsoft Edge — 分流规则说明

> 当前 Release 自动生成的服务说明。发行数字、Raw 地址、SHA-256 和图标身份均来自当前 SSOT。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| 显示名称 | **Microsoft Edge** |
| Service ID | `microsoftedge` |
| 类型 | 独立服务 |
| Provider / 服务集 | `microsoft` |
| 规则浏览路径 | `microsoft/microsoftedge/microsoftedge.yaml` |
| 语义规则数量 | **4** |
| 语义 SHA-256 | `527849a37d404a10404ca5ef3f756374dbb1c9390a47d765537d9058d1b05c9f` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Immutable Run | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |
| Icon Identity | `semantic.placeholder` |
| Icon Role | `strategy` |
| Icon Release | `2026.09.22-5e0e48ad55c6` |

## 2. 规则用途

这是 **Microsoft Edge 的独立服务规则**，可以作为独立远程规则集使用，不要求客户端同时加载其他同集服务。

不要仅根据服务名称、Provider、ASN、GeoIP 或历史规则推断未列出的域名/IP；Service Rule 与 Network Dataset 属于不同语义层。

## 3. 服务集与子服务

当前规则文件：
```text
rule/microsoft/microsoftedge/microsoftedge.yaml
```

所属服务集：[打开服务集](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/microsoft/README.md)

| 同服务集条目 | 类型 | 规则数 | 文档 |
|---|---|---:|---|
| `github` / GitHub | 独立服务 | 29 | [打开](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/microsoft/github/README.md) |
| `linkedin` / LinkedIn | 独立服务 | 12 | [打开](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/microsoft/linkedin/README.md) |
| `microsoft` / Microsoft | 服务集 / Provider 聚合 | 966 | [打开](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/microsoft/README.md) |
| `microsoftedge` / Microsoft Edge | 独立服务 | 4 | [打开](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/microsoft/microsoftedge/README.md) |
| `minecraft` / Minecraft | 独立服务 | 6 | [打开](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/microsoft/minecraft/README.md) |

## 4. 更新时间与发行状态

| 指标 | 当前值 |
|---|---|
| 数据更新日期 | **2026-09-24** |
| Release 生成时间 | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |
| 语义 rule_count | **4** |
| 客户端生成覆盖 | **7/7** |
| 客户端 rule_count 范围 | 0–4 |

> 当前 Manifest 只有 Release 级 Generated At，本页不伪造单文件更新时间。判断本服务是否变化，请比较 SHA-256。

## 5. 七客户端独立 Raw 订阅

| 客户端 | 实际文件 | rule_count | 大小(bytes) | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/microsoft/microsoftedge/microsoftedge.yaml` | 4 | 133 | `747af4c098f4d020045cf792850260b15816141126da90b441f94a204bd0a2bf` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/microsoft/microsoftedge/microsoftedge.yaml) |
| loon | `loon/microsoft/microsoftedge/microsoftedge.list` | 4 | 125 | `9775c3b021402322bfedecad925890b7be994bcf6706448bc010737c130af75c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/microsoft/microsoftedge/microsoftedge.list) |
| mihomo | `mihomo/microsoft/microsoftedge/microsoftedge.yaml` | 4 | 150 | `b74a4c79f3ac574db67fb509f803135e81d80fb1ca51260889e8a1184c827047` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/microsoft/microsoftedge/microsoftedge.yaml) |
| quantumultx | `quantumultx/microsoft/microsoftedge/microsoftedge.list` | 4 | 149 | `e7ad9bcaf098ea160685e3fc123b1907185f9e32e9dbaf35f1dc30bc414bcf6c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/microsoft/microsoftedge/microsoftedge.list) |
| shadowrocket | `shadowrocket/microsoft/microsoftedge/microsoftedge.list` | 4 | 125 | `9775c3b021402322bfedecad925890b7be994bcf6706448bc010737c130af75c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/microsoft/microsoftedge/microsoftedge.list) |
| singbox | `singbox/microsoft/microsoftedge/microsoftedge.json` | 0 | 215 | `b4f9d3db89c98fb7425e5c8deef224bb2dd496f0876602cf4669a185eec20bb7` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/microsoft/microsoftedge/microsoftedge.json) |
| surge | `surge/microsoft/microsoftedge/microsoftedge.list` | 4 | 125 | `9775c3b021402322bfedecad925890b7be994bcf6706448bc010737c130af75c` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/microsoft/microsoftedge/microsoftedge.list) |

### 5.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/microsoft/microsoftedge/microsoftedge.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/microsoft/microsoftedge/microsoftedge.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/microsoft/microsoftedge/microsoftedge.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/microsoft/microsoftedge/microsoftedge.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/microsoft/microsoftedge/microsoftedge.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/microsoft/microsoftedge/microsoftedge.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/microsoft/microsoftedge/microsoftedge.list`

## 6. 客户端使用方法

1. 选择你实际使用的客户端。
2. 复制本页该客户端专属 Raw 地址。
3. 在客户端的远程 Rule Set / Rule Provider / rule-set 功能中添加。
4. 按自己的配置把命中的规则交给 DIRECT / PROXY / REJECT 等策略。
5. 更新时重新拉取远程资源；自动化系统可通过 SHA-256 做缓存/变更检测。

### 6.1 Mihomo 示例
```yaml
rule-providers:
  microsoftedge:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/microsoft/microsoftedge/microsoftedge.yaml"
    path: ./ruleset/microsoftedge.yaml
    interval: 86400

rules:
  - RULE-SET,microsoftedge,PROXY
```

> 示例用于展示接入结构；实际 behavior / format / 策略组名称应与你使用的 Mihomo 版本和当前规则格式一致。

### 6.2 其他客户端

sing-box、Surge、Shadowrocket、Quantumult X、Egern、Loon：使用本页对应客户端的 Raw 地址，通过其支持的远程规则机制导入。不要跨客户端复用另一种格式的文件。

## 7. 服务集与独立子服务如何选择

**服务集：** 适合希望一次覆盖同一 Provider / 产品家族多个成员的场景。

**独立子服务：** 适合精确分流单一产品或子系统。直接使用该子服务的独立 Raw，不要从聚合文件手工复制、拆分、再发布。

**父级与子级同时加载：** 最终行为由客户端规则顺序决定；通常让更具体的子服务规则先于更宽泛的聚合规则。

## 8. 图标

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/placeholder.png" alt="Microsoft Edge icon" width="56" height="56">

| 属性 | 当前值 |
|---|---|
| Identity | `semantic.placeholder` |
| Role | `strategy` |
| Style / Size / Format | `minimal` / 128px / png |
| Icon Release | `2026.09.22-5e0e48ad55c6` |
| Icon Digest | `df792f3e1738dc253658bd9714d47a41dd91aa8a2cd0063185da91a817a90c09` |
| Icon Raw | [打开](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/placeholder.png) |

## 9. 完整性检查

| 检查项 | 权威来源 |
|---|---|
| Service ID / 路径 | `rule/_index.yaml` |
| 语义 rule_count / SHA-256 | `rule/_index.yaml` |
| 客户端文件 / rule_count / size / SHA-256 | `generated/manifest.json` |
| 更新时间 / Run / IR | `generated/manifest.json` + `rule/_index.yaml` |
| Icon Identity / Digest | Icon System 3 当前 client index |

**禁止手工修改派生发行物。** 规则变化应回到上游 / Canonical / 生产链，生成新的 Immutable Run。

## 10. 相关入口

- [服务总目录](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/SERVICE_CATALOG.md)
- [完整使用说明](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/RULE_USAGE_GUIDE.md)
- [规则索引](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/rule/_index.yaml)
- [Generated Manifest](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/generated/manifest.json)
- [Icon Usage](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/ICON_USAGE.md)

[回到顶部](#top)