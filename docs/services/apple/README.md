<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/apple.png" alt="Apple 图标" width="72" height="72">

# Apple — 分流规则说明

> 当前 Release 自动生成的服务说明。发行数字、Raw 地址、SHA-256 和图标身份均来自当前 SSOT。

## 1. 服务基本信息

| 项目 | 当前值 |
|---|---|
| 显示名称 | **Apple** |
| Service ID | `apple` |
| 类型 | 服务集 / Provider 聚合 |
| Provider / 服务集 | `apple` |
| 规则浏览路径 | `apple/apple.yaml` |
| 语义规则数量 | **2027** |
| 语义 SHA-256 | `102f86011902e2ea9b7b77bca54fc3b7ac30467c451d68c6dbf773b947680dcf` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Immutable Run | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |
| Icon Identity | `brand.apple` |
| Icon Role | `service` |
| Icon Release | `2026.09.22-5e0e48ad55c6` |

## 2. 规则用途

这是 **Apple 服务集的聚合规则**，用于一次覆盖该服务集当前已登记的相关规则。需要更精确分流时，应直接使用下方独立子服务，而不是手工拆分聚合文件。

不要仅根据服务名称、Provider、ASN、GeoIP 或历史规则推断未列出的域名/IP；Service Rule 与 Network Dataset 属于不同语义层。

## 3. 服务集与子服务

当前规则文件：
```text
rule/apple/apple.yaml
```

这是顶级服务集 **apple** 的入口，共 6 个已登记规则条目。

| 同服务集条目 | 类型 | 规则数 | 文档 |
|---|---|---:|---|
| `apple` / Apple | 服务集 / Provider 聚合 | 2027 | [打开](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/apple/README.md) |
| `applefirmware` / Apple Firmware | 独立服务 | 175 | [打开](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/apple/applefirmware/README.md) |
| `appleid` / Apple ID | 独立服务 | 4 | [打开](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/apple/appleid/README.md) |
| `applemail` / Apple Mail | 独立服务 | 2 | [打开](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/apple/applemail/README.md) |
| `appletv` / Apple TV | 独立服务 | 7 | [打开](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/apple/appletv/README.md) |
| `icloudprivaterelay` / iCloud Private Relay | 独立服务 | 6 | [打开](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/apple/icloudprivaterelay/README.md) |

## 4. 更新时间与发行状态

| 指标 | 当前值 |
|---|---|
| 数据更新日期 | **2026-09-24** |
| Release 生成时间 | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |
| 语义 rule_count | **2027** |
| 客户端生成覆盖 | **7/7** |
| 客户端 rule_count 范围 | 0–2014 |

> 当前 Manifest 只有 Release 级 Generated At，本页不伪造单文件更新时间。判断本服务是否变化，请比较 SHA-256。

## 5. 七客户端独立 Raw 订阅

| 客户端 | 实际文件 | rule_count | 大小(bytes) | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/apple/apple.yaml` | 2014 | 51088 | `8ae3a18902d2c3325b1e72cb7755e8ae2e27fc2bfaf8d41151eda28dc26be42a` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/apple/apple.yaml) |
| loon | `loon/apple/apple.list` | 2014 | 65837 | `2797a21bd5710008955fc74051883a8a3d39cdaf4c0c161cbe702db394150088` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/apple/apple.list) |
| mihomo | `mihomo/apple/apple.yaml` | 2014 | 73902 | `10381458e8e9a8f0bddea48f5cbe181bdeda4674908241133f103681b4ff55c0` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/apple/apple.yaml) |
| quantumultx | `quantumultx/apple/apple.list` | 2014 | 77947 | `5b37a5087e122749d052bf09ff6fc8740be182024db8c673e97a8cbdca74963d` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/apple/apple.list) |
| shadowrocket | `shadowrocket/apple/apple.list` | 2014 | 65837 | `2797a21bd5710008955fc74051883a8a3d39cdaf4c0c161cbe702db394150088` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/apple/apple.list) |
| singbox | `singbox/apple/apple.json` | 0 | 61248 | `4edec38d1478f2fc6563e5429322cace081909f21526df22f98df5a1dfc47666` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/apple/apple.json) |
| surge | `surge/apple/apple.list` | 2014 | 65837 | `2797a21bd5710008955fc74051883a8a3d39cdaf4c0c161cbe702db394150088` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/apple/apple.list) |

### 5.1 Raw 地址直接复制

- **egern**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/apple/apple.yaml`
- **loon**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/apple/apple.list`
- **mihomo**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/apple/apple.yaml`
- **quantumultx**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/apple/apple.list`
- **shadowrocket**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/apple/apple.list`
- **singbox**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/apple/apple.json`
- **surge**：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/apple/apple.list`

## 6. 客户端使用方法

1. 选择你实际使用的客户端。
2. 复制本页该客户端专属 Raw 地址。
3. 在客户端的远程 Rule Set / Rule Provider / rule-set 功能中添加。
4. 按自己的配置把命中的规则交给 DIRECT / PROXY / REJECT 等策略。
5. 更新时重新拉取远程资源；自动化系统可通过 SHA-256 做缓存/变更检测。

### 6.1 Mihomo 示例
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

> 示例用于展示接入结构；实际 behavior / format / 策略组名称应与你使用的 Mihomo 版本和当前规则格式一致。

### 6.2 其他客户端

sing-box、Surge、Shadowrocket、Quantumult X、Egern、Loon：使用本页对应客户端的 Raw 地址，通过其支持的远程规则机制导入。不要跨客户端复用另一种格式的文件。

## 7. 服务集与独立子服务如何选择

**服务集：** 适合希望一次覆盖同一 Provider / 产品家族多个成员的场景。

**独立子服务：** 适合精确分流单一产品或子系统。直接使用该子服务的独立 Raw，不要从聚合文件手工复制、拆分、再发布。

**父级与子级同时加载：** 最终行为由客户端规则顺序决定；通常让更具体的子服务规则先于更宽泛的聚合规则。

## 8. 图标

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/apple.png" alt="Apple icon" width="56" height="56">

| 属性 | 当前值 |
|---|---|
| Identity | `brand.apple` |
| Role | `service` |
| Style / Size / Format | `minimal` / 128px / png |
| Icon Release | `2026.09.22-5e0e48ad55c6` |
| Icon Digest | `2be4f77df5e8f4b6486da4ce9fff209a8e7888f065d0f4e1812c24fcefee707a` |
| Icon Raw | [打开](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/clients/mihomo/128/apple.png) |

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