# P3 长期能力：可审计规则编译系统

P3 在 V3 Canonical → IR → Adapter 之上建立 release evidence 层，把一次构建升级为可追踪、可验证、可回滚的发布单元。

## 能力矩阵

| 能力 | 实现 | 主要证据 |
|---|---|---|
| Rule semantic diff | `semantic_rule_diff()` | `rule_semantic_diff_v1` |
| Adapter capability matrix | `adapter_capability_matrix()` | `adapter_capability_matrix_v1` |
| Source health scoring | `source_health_score()` | `source_health_v1` |
| Provenance graph | `build_provenance_graph()` | `provenance_graph_v1` |
| Release manifest | `write_release_manifest()` | `release_manifest_v1` |
| SBOM | `generate_sbom()` | CycloneDX 1.5 JSON |
| Dependency lock | `dependency_lock_report()` | `dependency_lock_v1` |
| Artifact checksum | `write_checksum_manifest()` | SHA-256 |
| Action SHA verification | `verify_action_shas()` | `action_sha_verification_v1` |

## 审计链

```text
source health
    ↓
canonical / semantic diff
    ↓
IR + adapter capability matrix
    ↓
artifact + provenance graph
    ↓
SHA-256 checksums + SBOM + dependency lock
    ↓
release manifest
    ↓
rollback = checkout exact commit
```

核心原则：审计数据与产物解耦；所有判定函数是标准库实现；工作流在 PR / main 上执行供应链门禁。`requirements.lock` 保持 exact pin，Actions 使用 40 位 commit SHA 固定引用。
