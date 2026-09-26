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
## 图标体系\n\n[Icon Library V4：10 层视觉矩阵](docs/ICON_STYLE_GUIDE_V4.md) · [V4 图标库](assets/icons/v4/README.md)\n\n## 当前发行状态

| 指标 | 当前值 |
|---|---|
| Collection Date | **2026-09-24** |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Immutable Run | `20260924T043120249584Z-run` |
| Semantic IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |
| 规则索引条目 | **262** |
| 顶级服务集 | **116** |
| Generated 文件 | **1984** |
| 客户端 | **7** |
| Icon Release | `2026.09.25-prc-icon-matrix-3` |

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

- [服务规则目录](docs/SERVICE_CATALOG.md)
- [规则完整使用说明](docs/RULE_USAGE_GUIDE.md)
- [文档一致性审计](docs/DOCUMENTATION_AUDIT.md)
- [生产规则链](docs/PRODUCTION_RULE_CHAIN.md)
- [Generated Outputs](docs/GENERATED_OUTPUTS.md)
- [Network Datasets](docs/NETWORK_DATASETS.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Icon Usage](docs/ICON_USAGE.md)

> `rule/` 与 `generated/` 都是派生发行物。不要手工修补规则数字、Raw URL、SHA-256 或图标路径。