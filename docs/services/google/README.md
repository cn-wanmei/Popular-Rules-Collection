<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/google.png" alt="Google 图标" width="72" height="72">

# Google — 分流规则说明

> 当前 Release 自动生成的服务说明。发行数字、Raw 地址、SHA-256 和图标身份均来自当前 SSOT。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| 显示名称 | **Google** |
| Service ID | `google` |
| 类型 | 服务集 / Provider 聚合 |
| Provider / 服务集 | `google` |
| 规则浏览路径 | `google/google.yaml` |
| 语义规则数量 | **1469** |
| 语义 SHA-256 | `92a652dc26d47108fc3ff3f0d987776865db17b069149184c4b805158d9f74f3` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Immutable Run | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |
| Icon Identity | `brand.google` |
| Icon Role | `service` |
| Icon Release | `2026.09.22-5e0e48ad55c6` |

## 2. 规则用途

这是 **Google 服务集的聚合规则**，用于一次覆盖该服务集当前已登记的相关规则。需要更精确分流时，应直接使用下方独立子服务，而不是手工拆分聚合文件。

不要仅根据服务名称、Provider、ASN、GeoIP 或历史规则推断未列出的域名/IP；Service Rule 与 Network Dataset 属于不同语义层。

## 3. 服务集与子服务

当前规则文件：
```text
rule/google/google.yaml
```

这是顶级服务集 **google** 的入口，共 8 个已登记规则条目。

| 同服务集条目 | 类型 | 规则数 | 文档 |
|---|---|---:|---|
| `firebase` / Firebase | 独立服务 | 2 | [打开](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/google/firebase/README.md) |
| `google-search` / Google Search | 独立服务 | 1 | [打开](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/google/google-search/README.md) |
| `google` / Google | 服务集 / Provider 聚合 | 1469 | [打开](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/google/README.md) |
| `googlecloud` / Google Cloud | 独立服务 | 5 | [打开](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/google/googlecloud/README.md) |
| `googleearth` / Google Earth | 独立服务 | 16 | [打开](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/google/googleearth/README.md) |
| `googlefcm` / Google FCM | 独立服务 | 13 | [打开](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/google/googlefcm/README.md) |
| `googlevoice` / Google Voice | 独立服务 | 1 | [打开](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/google/googlevoice/README.md) |
| `scholar` / Google Scholar | 独立服务 | 231 | [打开](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/google/scholar/README.md) |

## 4. 更新时间与发行状态

| 指标 | 当前值 |
|---|---|
| 数据更新日期 | **2026-09-24** |
| Release 生成时间 | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |
| 语义 rule_count | **1469** |
| 客户端生成覆盖 | **7/7** |
| 客户端 rule_count 范围 | 0–1463 |

> 当前 Manifest 只有 Release 级 Generated At，本页不伪造单文件更新时间。判断本服务是否变化，请比较 SHA-256。

## 5. 七客户端独立 Raw 订阅

| 客户端 | 实际文件 | rule_count | 大小(bytes) | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/google/google.yaml` | 1463 | 31790 | `c69fd8dc4b8b9acf83998eddefb3cd1aa38df2ac1e28f7b3dbb117435551eb37` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/google/google.yaml) |
| loon | `loon/google/google.list` | 1463 | 42650 | `a759912e89df297b06ee5b1d74b864af388f14de87faa0b9a75fff303c9a5ca2` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/google/google.list) |
| mihomo | `mihomo/google/google.yaml` | 1463 | 48511 | `f5144b4d646aba8d8712426ccf877736e521db8116330e975a336819fdd41141` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/google/google.yaml) |
| quantumultx | `quantumultx/google/google.list` | 1463 | 51438 | `ed65c1041b4dcbb9e8bd0e8caa1c095b9d7e007e005ff54d2cc835643a0c812a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/google/google.list) |
| shadowrocket | `shadowrocket/google/google.list` | 1463 | 42650 | `a759912e89df297b06ee5b1d74b864af388f14de87faa0b9a75fff303c9a5ca2` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/google/google.list) |
| singbox | `singbox/google/google.json` | 0 | 39195 | `a36e0c857947a2072ab7e4eb059a080fee4d897388876158f1766ecc1333c18a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/google/google.json) |
| surge | `surge/google/google.list` | 1463 | 42650 | `a759912e89df297b06ee5b1d74b864af388f14de87faa0b9a75fff303c9a5ca2` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/google/google.list) |

### 5.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/google/google.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/google/google.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/google/google.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/google/google.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/google/google.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/google/google.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/google/google.list`

## 6. 客户端使用方法

1. 选择你实际使用的客户端。
2. 复制本页该客户端专属 Raw 地址。
3. 在客户端的远程 Rule Set / Rule Provider / rule-set 功能中添加。
4. 按自己的配置把命中的规则交给 DIRECT / PROXY / REJECT 等策略。
5. 更新时重新拉取远程资源；自动化系统可通过 SHA-256 做缓存/变更检测。

### 6.1 Mihomo 示例
```yaml
rule-providers:
  google:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/google/google.yaml"
    path: ./ruleset/google.yaml
    interval: 86400

rules:
  - RULE-SET,google,PROXY
```

> 示例用于展示接入结构；实际 behavior / format / 策略组名称应与你使用的 Mihomo 版本和当前规则格式一致。

### 6.2 其他客户端

sing-box、Surge、Shadowrocket、Quantumult X、Egern、Loon：使用本页对应客户端的 Raw 地址，通过其支持的远程规则机制导入。不要跨客户端复用另一种格式的文件。

## 7. 服务集与独立子服务如何选择

**服务集：** 适合希望一次覆盖同一 Provider / 产品家族多个成员的场景。

**独立子服务：** 适合精确分流单一产品或子系统。直接使用该子服务的独立 Raw，不要从聚合文件手工复制、拆分、再发布。

**父级与子级同时加载：** 最终行为由客户端规则顺序决定；通常让更具体的子服务规则先于更宽泛的聚合规则。

## 8. 图标

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/google.png" alt="Google icon" width="56" height="56">

| 属性 | 当前值 |
|---|---|
| Identity | `brand.google` |
| Role | `service` |
| Style / Size / Format | `minimal` / 128px / png |
| Icon Release | `2026.09.22-5e0e48ad55c6` |
| Icon Digest | `abf2f545e8cdaf74d5e3c362f0bd909b62b1c9964e64acace988a4d63e56d733` |
| Icon Raw | [打开](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/google.png) |

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