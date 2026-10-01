# Phase O-R — Operational Closure Reconciliation

Phase O-R 是对 Phase N/O “代码已经合并、运行时证据尚未形成闭环”的操作性补丁，不是新的业务数据阶段。

## 核心原则

- 不接受 --runs 3 作为观察证据。
- 状态只来自持久化 reports/v1/PHASE_O_STATE.json。
- 证据只来自持久化 reports/v1/PHASE_O_EVIDENCE_BUNDLE.json。
- 每次 observation 必须绑定 run_id、snapshot_id、cutover commit SHA，并提供 seven-client、golden、determinism、artifact equivalence、semantic regression、source health 六类证据。
- Phase O-R、Phase O 均禁止移动、删除或自动退休旧 rule/ 根。

## 状态机

NOT_EXECUTED -> CUTOVER_EXECUTED -> OBSERVING -> FROZEN_OLD_ROOT -> RETIRED

- NOT_EXECUTED -> CUTOVER_EXECUTED：需要持久化 cutover 事实。
- CUTOVER_EXECUTED -> OBSERVING：需要至少 3 个真实、切换后的完整运行。
- OBSERVING -> FROZEN_OLD_ROOT：上述 3 个运行全部合格，并存在旧根冻结证据。
- FROZEN_OLD_ROOT -> RETIRED：需要明确人工批准；脚本不得自动删除旧根。

## 当前状态

初始持久化状态仍为 NOT_EXECUTED。当前主线运行时仍使用 rule/，rules/ 尚未成为生产 Canonical Root，因此本提交不会伪造切换或观察完成。

## Evidence Bundle

每个 observation run 至少提供：

run_id
snapshot_id
post_cutover: true
cutover_commit_sha
checks:
  seven_client: true
  golden: true
  determinism: true
  artifact_equivalence: true
  semantic_regression: true
  source_health: true
references:
  run_manifest:
  observation:
  golden:
  artifacts:
  determinism:
  artifact_equivalence:
  semantic_regression:
  source_health:

同一个 run_id 或 snapshot_id 不得重复计数。

## 与 Phase N/O 的关系

Phase N 负责一次性 runtime cutover；Phase O-R 负责证明切换事实已经持久化，并把运行观察绑定到切换后的真实运行；Phase O 负责观察期后的 freeze/retirement gate。

因此在 O-R 未闭环之前，不得把 Phase O 的 FROZEN_OLD_ROOT 或 RETIRED 写成完成。
