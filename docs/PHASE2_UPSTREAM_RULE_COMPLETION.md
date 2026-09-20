# Phase 2 — 上游规则缺失补全与双仓生产接入

## 目标

在不改变当前 V3 生产模型的前提下，把 Popular-Rules-Source 建设为可持续补全缺失 Service Domain 的上游 Source。

## 双仓职责

~~~text
Popular-Rules-Source
  ├─ Official Source
  ├─ Evidence
  ├─ Boundary / Exclusion
  ├─ Materialization
  └─ Immutable Source Release
             ↓
Popular-Rules-Collection
  ├─ Registry
  ├─ Canonical
  ├─ IR
  ├─ 7 clients
  ├─ Golden
  └─ Production Publish
~~~

## 缺失规则补全

~~~text
Gap Audit
  ↓
Official Discovery
  ↓
Candidate
  ↓
Evidence
  ↓
Boundary / Exclusion
  ↓
Conflict
  ↓
Verified Source
  ↓
Immutable Snapshot
  ↓
Collection Reconciliation
  ↓
Canary
  ↓
Production
~~~

第三方规则只能做交叉验证，不能单独进入生产。

## Canary Contract

PRS：

~~~yaml
enabled: false
~~~

必须按 Service 独立启用，不能一次性打开全部首批服务。

单服务启用要求：

1. Source Release Schema PASS
2. seed-only = 0
3. Evidence linkage PASS
4. Boundary / Exclusion PASS
5. Conflict = 0
6. Determinism PASS
7. Collection ingest PASS
8. V3 Build PASS
9. 7-client semantic PASS
10. Rollback rehearsal PASS

## 回滚

~~~text
disable service
  ↓
restore previous Source Snapshot
  ↓
re-run V3
  ↓
verify generated compatibility
~~~

不改历史 Snapshot。

## Phase 2 并行

Source 可按服务并行实施：

- Official Source Adapter
- Missing-rule Candidate Ledger
- Evidence / Boundary
- Snapshot / Release
- Service-level CI

Collection 同时实施：

- Source Registry Canary
- Reconciliation
- V3 integration
- 7-client semantic regression
- rollback pointer

两个仓库通过 Release Contract 解耦，不要求同一天完成。

## Main Replacement

Phase 2 正常生产后，推荐：

~~~text
Frozen main
  ↓
Green Phase 2 PR
  ↓
Review + required checks
  ↓
merge / fast-forward
  ↓
resume production writers
~~~

不把 force-push / ref replacement 作为正常生产切换方式。

## Phase 2 Exit

- 首个 official-evidence-only Source Release
- Source ↔ Collection Reconciliation 稳定
- V3 full build PASS
- 7-client semantic PASS
- rollback 验证通过
- observation window 启动

“8/8 Published”不是唯一结束条件。
