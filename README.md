# Popular-Rules-Collection

> 面向 **Mihomo / sing-box / Surge / Shadowrocket / Quantumult X / Egern / Loon** 的规则数据生产、服务目录与客户端发行项目。

## 快速入口

<small>

| 类型 | 入口 | 用途 |
|---|---|---|
| 服务规则 | [rule/](rule/README.md) | 浏览、选择服务规则 |
| 客户端规则 | [generated/](generated/manifest.json) | 客户端直接使用 |
| 服务目录 | [SERVICE_CATALOG](docs/SERVICE_CATALOG.md) | 查找服务 / 子服务 |
| 服务说明 | [docs/services/](docs/services/) | Raw、统计与图标 |
| 目录规范 | [docs/layout.md](docs/layout.md) | Directory Layout v2 |

</small>

## 图标体系

[Icon System 6.0](https://github.com/cn-wanmei/Popular-Rules-Icon) · [V6 切换状态](docs/ICON_V6_CUTOVER.md) · V5 已从运行时与物理资产中完全退休

## 当前项目状态

| 项目 | 状态 |
|---|---|
| 服务身份权威 | Collection `rule/_index.yaml` |
| Canonical service | **394** |
| Icon V6 active provider | **v6** |
| V6 manifest | `icon-2026.09.30.clean1` |
| Canonical service coverage | **394/394 (100%)** |
| V6 orphan entries | **0** |
| AI canonical service | **已补齐** |
| V5 fallback | **disabled / retired** |
| V5 physical assets | **deleted** |
| V6 clean production writer | **PASS** |

> 当前不应把历史 262 条规则、146 service、V5/V4 icon coverage 当作 2026-09-30 的实时状态。

## 当前发行状态

> **权威实时状态**：根目录 [`PUBLISH_STATUS.md`](PUBLISH_STATUS.md)（由 `status.yml` CI 自动生成，含 snapshot 日期、Collection ID、Source health、客户端输出）。**请勿在 README 手写这些数字。**
>
> 客户端固定为 7 套：egern / loon / mihomo / quantumultx / shadowrocket / singbox / surge。  
> Icon V6 production release 与回滚 ID 以 [`config/icon_v6.yaml`](config/icon_v6.yaml) 及 Icon 仓 `config/release-pointers.yaml` 为准。

## 七客户端发行目录

| 客户端 | 实际目录 | 格式 |
|---|---|---|
| Mihomo | `generated/mihomo/` | YAML |
| sing-box | `generated/singbox/` | JSON |
| Surge | `generated/surge/` | LIST |
| Shadowrocket | `generated/shadowrocket/` | LIST |
| Quantumult X | `generated/quantumultx/` | LIST |
| Egern | `generated/egern/` | YAML |
| Loon | `generated/loon/` | LIST |

## 服务快速目录

> 每个服务 / 子服务均有独立说明页；打开后可直接复制对应客户端 Raw，并查看规则数、更新时间、SHA-256 与图标。

<!-- SERVICE_DIRECTORY:START -->

<small>完整服务 / 子服务目录请进入 [SERVICE_CATALOG.md](docs/SERVICE_CATALOG.md)。首页仅保留入口，避免全量链接重复展开。</small>

<!-- SERVICE_DIRECTORY:END -->

## 目录边界

| 路径 | 职责 |
|---|---|
| `data/runs/<run>/canonical/` | V3 Canonical 真源 |
| `data/runs/<run>/ir/` | Semantic IR |
| `rule/` | 人类浏览 / 搜索 / 选择发行树 |
| `generated/<client>/` | 客户端编译规则 |
| `generated/<network-scope>/` | Network Dataset |
| `docs/services/` | 服务 / 子服务独立说明 |
| `docs/SERVICE_CATALOG.md` | 全量服务目录 |
| `docs/archive/activation/` | 历史冻结 / 激活证据（非当前策略） |

## 生产链

```text
Upstream
  ↓
Collect → immutable backup/<date>
  ↓
V3 Engine
  ↓
Canonical → Semantic IR
  ├── rule/               人类浏览 / 服务选择
  └── generated/          7 客户端 + Network Dataset
  ↓
Gates → Immutable Release Candidate → Publish
```

## 文档

- [文档索引](docs/INDEX.md)
- [服务规则目录](docs/SERVICE_CATALOG.md)
- [规则完整使用说明](docs/RULE_USAGE_GUIDE.md)
- [文档一致性审计](docs/DOCUMENTATION_AUDIT.md)
- [生产规则链](docs/PRODUCTION_RULE_CHAIN.md)
- [Generated Outputs](docs/GENERATED_OUTPUTS.md)
- [Network Datasets](docs/NETWORK_DATASETS.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Icon System 6.0（外部）](https://github.com/cn-wanmei/Popular-Rules-Icon)
- [V6 切换状态](docs/ICON_V6_CUTOVER.md)
- [历史激活档案](docs/archive/activation/README.md)

> `rule/` 与 `generated/` 都是派生发行物。不要手工修补规则数字、Raw URL、SHA-256 或图标路径。

> V5 runtime provider/configuration and physical legacy assets have been fully retired after the final gate.

> 根目录若仍有 freeze/activation **存根**，仅作重定向；正文与证据在 `docs/archive/activation/`。策略以当前 SSOT 与 CI 为准，勿把存根当现行策略。
