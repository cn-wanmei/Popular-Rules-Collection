# Phase 2 — 上游规则缺失补全与双仓生产接入

## 目标

在不破坏当前 V3 生产链的前提下，把 Popular-Rules-Source 建设为可持续补全缺失 Service Domain 的上游 Source。

## 双仓职责

~~~text
Popular-Rules-Source
  ├─ Official Source
  ├─ Evidence
  ├─ Boundary
  ├─ Materialization
  └─ Immutable Release
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
Snapshot
  ↓
Collection Reconciliation
  ↓
Canary
  ↓
Production
~~~

## Canary Contract

PRS：

~~~yaml
enabled: false
~~~

按 service 独立启用，不允许一次性打开全部首批服务。

单服务启用必须通过：

1. Source Release Schema
2. Seed-only = 0
3. Evidence linkage
4. Boundary / Exclusion
5. Conflict = 0
6. Determinism
7. Collection ingest
8. V3 Build
9. 7-client semantic
10. rollback rehearsal

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

不修改历史 Snapshot。

## Main Replacement

正常路径不是 force-replace：

~~~text
Frozen main
   ↓
Green Phase 2 PR
   ↓
Review + Gate
   ↓
merge / fast-forward
   ↓
normal production main
~~~

Force ref replacement 仅作为异常恢复手段。

## 第二阶段完成标准

不是规则数量，而是：

- 首个 official-evidence-only Source Release
- Source ↔ Collection 对账稳定
- V3 全链通过
- 7 客户端语义一致
- 可回滚
- production observation 已启动
