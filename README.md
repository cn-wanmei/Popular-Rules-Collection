# Popular-Rules-Collection

> 面向 Mihomo / sing-box / Surge / Shadowrocket / Quantumult X / Egern / Loon 的规则数据生产、服务目录与客户端发行项目。

## 图标体系

[Icon System 6.0](https://github.com/cn-wanmei/Popular-Rules-Icon) · [V6 最终切换](docs/ICON_V6_CUTOVER.md)

## 当前项目状态（2026-09-30）

| 项目 | 当前状态 |
|---|---|
| 服务身份权威 | `rule/_index.yaml` |
| Canonical service | **394** |
| Icon provider | **V6** |
| Active release | `icon-2026.09.30.clean1` |
| Canonical coverage | **394/394** |
| Production orphan identities | **0** |
| V6 release-writer | **已验证成功** |
| V6 physical closure | **6304/6304** |
| V5 fallback | **已关闭** |
| V5 local asset tree | **待最终 gate 后删除** |
| V5 rollback dependency | **无** |

## 服务规则目录

- [服务规则目录](docs/SERVICE_CATALOG.md)
- [规则完整使用说明](docs/RULE_USAGE_GUIDE.md)
- [生产规则链](docs/PRODUCTION_RULE_CHAIN.md)
- [Generated Outputs](docs/GENERATED_OUTPUTS.md)
- [Icon Usage](docs/ICON_USAGE.md)

## 图标生产关系

```text
Collection canonical service
        ↓
Icon identity snapshot
        ↓
Icon state / acquisition
        ↓
V6 release writer
        ↓
immutable dist release
        ↓
Collection resolver
        ↓
client icon URL
```

> `rule/` 与 `generated/` 都是派生发行物。不要手工修改规则数字、SHA-256、Raw URL 或图标路径。
