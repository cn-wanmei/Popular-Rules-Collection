# 数字单一事实源（C）

> **禁止**在 README / 发行说明中手写 canonical 服务数、规则条目、Source health。

| 数字 | 权威位置 |
|---|---|
| 用户可见服务身份 (`entity: service`) | Collection `rule/_index.yaml` |
| `_index` 全实体（含 aggregate） | 同上；**不得**与 Icon coverage 直接对比 |
| 发行/CI 状态 | `PUBLISH_STATUS.md`（CI 自动刷新） |
| Source 证据生命周期 | Source `config/source_canary_state.yaml` |
| Icon production / coverage | Icon `config/release-pointers.yaml` + identity snapshot |

## 口径说明（2026-10-06 交叉审计锁定）

- **Source lifecycle ≠ Collection production**
- `_index.yaml` 典型构成（示例量级，以实际文件为准）：
  - `entity: service` ≈ **394** ← **Icon 与对外「canonical service」只计此项**
  - `entity: provider_aggregate` ≈ **254**
  - 其他 aggregate / category 少量
  - **合计**可到 **651**（Release notes 中的 “Canonical services (rule/_index)” 若指全 entries，必须注明口径）
- Icon `collection_identity_snapshot.json` 的 `selection` **exclude** `provider_aggregate` / `aggregate` / `domestic_aggregate` / `category`
- 因此 **Icon 394/394 = 100% of services**，与 651 全实体数对比是**错误口径**，不是覆盖缺口

## 检查

```bash
# Collection — 禁止 README 硬编码数字
grep -nE '[0-9]{3,}' README.md || true

# 按 entity 统计（需 PyYAML）
python -c "import yaml; d=yaml.safe_load(open('rule/_index.yaml')); from collections import Counter; c=Counter(e.get('entity') for e in d['entries']); print(dict(c), 'total', sum(c.values()))"
```
