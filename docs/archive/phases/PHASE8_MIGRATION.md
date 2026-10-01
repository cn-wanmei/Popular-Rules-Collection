# Phase 8 — Formal Migration (ordered)

## Hard order

```text
1. 补全规则集（物化 或 intentional 登记）
2. Coverage == 100%
3. 正式迁移：Legacy → V1 Canonical 为唯一 SoT
4. 最后才允许删除 Legacy Source
```

**禁止**在 Coverage 未满或存在未解释 Removed 时切换 SoT 或删除 Legacy。

## Coverage 公式（SSOT）

```text
Daily Coverage =
  (materialized + intentional_unmaterialized) / registered
```

Intentional codes（`config/intentional_unmaterialized.yaml`）：

| Code | Meaning |
|------|---------|
| `NO_UPSTREAM` | 无已验证专用规则集 |
| `COVERED_BY_AGGREGATE` | 由父级/生态聚合覆盖 |
| `MAPS_TO` | 别名，映射到另一 service id |
| `DEFERRED_PROFILE` | 有意延期的 profile |
| `KEYWORD_ONLY` | 仅 keyword / 空 domain 集（设计如此） |
| `SOURCE_DRIFT` | 上游路径变更，待重绑 |

**禁止**为 intentional 条目伪造 domain。

## 模块

| 模块 | 职责 |
|------|------|
| `src/engine/v1/phase8.py` | Coverage 计算、intentional 校验、门禁、SoT 切换授权、Legacy 删除授权 |
| `src/engine/v1/legacy_regression.py` | Removed 必须可解释（Phase 7） |
| `config/intentional_unmaterialized.yaml` | intentional SSOT |

## 门禁

1. `intentional_registry_valid` — code ∈ 枚举且有 reason  
2. `coverage_100` — missing 列表为空  
3. `no_unexplained_removed` — Phase 7 无未解释 Removed  
4. `graph_acyclic` — Phase 3.2 无环  
5. `golden_gate` — Phase 4 Golden 结构覆盖通过  

全部通过 → `stage=ready`。  
`switch_sot_to_v1()` → `sot=v1_canonical`。  
`request_legacy_delete(allow_legacy_delete=True)` → 仅授权，不直接删文件。

## 删除 Legacy

必须同时满足：

- `sot == v1_canonical`
- 全部门禁仍为绿
- 操作者显式 `allow_legacy_delete=True`

实际删目录由独立运维脚本执行，并再次读取 Phase 8 报告中的授权标志。
