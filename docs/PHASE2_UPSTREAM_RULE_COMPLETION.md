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


## Collection-side content reconciliation

Canary 不只验证“Registry 已登记”，还必须完成内容级绑定：

- Source snapshot 的 `domains.txt` 与 snapshot manifest 的 domain set 完全一致。
- Source Release 的 `snapshot_id` 与 `content_digest` 必须同时绑定。
- Collection PRS registry 必须存在对应 service，且全局与 service entry 都保持 disabled。
- Canary `source-binding.json` 必须精确绑定 Source commit、snapshot、content digest 与 domain count。
- Collection Canary input 与 V3 Semantic IR 的 domain rule set 必须与 Source snapshot 完全一致。
- 生成 deterministic `reconciliation_run_id`，写入 Canary evidence；缺失或非 PASS 不得进入下一阶段。

## Observation window

Reconciliation、V3、7-client semantic、rollback 全部真实通过后，Canary 才能创建 Observation evidence。

Observation 是非晋级证据：

- 记录实际 `observation_started_at` 与 deterministic `observation_run_id`。
- `promotes: false`。
- 不修改 `source_canary_state.yaml`。
- 不启用 PRS。
- 不恢复 Production writer。

## Production Unlock qualification

Production Unlock 使用独立的 fail-closed gate 读取 Policy、Canary Attestation 与 Canary report，只做资格判断，不执行生产写操作。

必须同时满足：

- official Source Release 已验证且 exact commit/snapshot/digest 有绑定；
- Collection reconciliation PASS；
- V3 build / Golden PASS；
- 7 个客户端 semantic 全部 PASS；
- rollback rehearsal PASS；
- Observation window 已实际启动；
- PRS global enabled 仍为 false；
- 当前服务状态仍为 `canary`，不会由 gate 自动改写为 `production`。

因此，`PASSED` Attestation 或 Unlock Gate PASS 只表示“满足生产解锁前置条件”，不等价于已经执行生产切换。
