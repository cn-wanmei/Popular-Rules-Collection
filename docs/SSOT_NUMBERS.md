# 数字单一事实源（C）

> **禁止**在 README / 发行说明中手写 canonical 服务数、规则条目、Source health。

| 数字 | 权威位置 |
|---|---|
| 用户可见服务身份 | Collection `rule/_index.yaml`（`entity: service`） |
| 发行/CI 状态 | `PUBLISH_STATUS.md`（CI 自动刷新） |
| Source 证据生命周期 | Source README 生成表 / `config/source_canary_state.yaml` |
| Icon production | Icon `config/release-pointers.yaml` |

## 口径说明

- **Source lifecycle ≠ Collection production**
- `_index` 可能含 service + provider_aggregate + aggregate；对外「canonical service」只计 `entity: service`
- Release notes 中的服务数以打包时解析的 index 为准，并应与当时 `PUBLISH_STATUS` 一致

## 检查

```bash
# Collection
grep -n 'Canonical service' README.md   # 若硬编码数字，改为链到 PUBLISH_STATUS
```
