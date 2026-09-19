# Phase I–O 执行总计划

> 原则：**先修验收系统，再修 P0 数据，再做 Canonical 迁移。**

## 开发并行、运行串行

I–O 允许并行开发分支，但生产执行必须服从依赖链：

I → J/K → L → M → N → O-R → O

其中 J、K、L 可在 I 的控制面契约确认后并行完善；M、N、O-R、O 可以并行编写执行器，但在前置证据未闭合时必须 fail-closed。

## Phase I — Gate Closure

修复验收层自身的假绿风险：

- C：37 条注册项 = 34 intentional-only + 3 materialized-and-intentional。
- E：Dual-Track 以 Service/Asset/Dependency/Aggregate/IR/Artifact 语义等价为准，不以路径同名为准。
- G：Determinism 必须绑定当前 HEAD、run_id、snapshot_id 与 Canonical/Artifact 证据。
- A：输出带 HEAD、run、snapshot、canonical digest、client digests 的基线。
- Directory Gate：目标 rules/ 的“存在性/非空性”只在迁移阶段开启，避免当前设计阶段假绿。

## Phase J — P0 50 Service

P0 固定为 50 个 Service，分为 5 × 10 批次。每个 Service 必须同时通过 identity/source/canonical/semantic/overlap/seven-client/golden/release 八个硬门禁。

当前生产矩阵不能通过改 status 文件直接变成 production；必须由证据驱动。

## Phase K — Intentional 最终定案

固定 registry 语义为：

- registry_total = 37
- intentional_only = 34
- materialized_and_intentional = 3

该分类用于审计与历史可追溯性，不等同于“缺失规则”。

## Phase L — Canonical Contract Freeze

冻结唯一物理目标：

rules/{provider}/all
rules/{provider}/{service}
rules/china/all

冻结只锁设计，不切换运行时、不填充目标目录、不删除旧源。

## Phase M — 真正 Dual-Track

从 Canonical Service Model 生成 rules/，同时保持 rule/ 为运行时源。

必须生成双轨 semantic inventory，并验证：

- Service identity
- Asset identity
- Membership
- Dependency closure
- Aggregate closure
- Network references
- Final IR digest
- Artifact digest

## Phase N — Runtime Cutover

仅允许一次明确的 cutover commit：

1. loader 切到 rules/
2. CI/publish 监控切到 rules/**
3. 旧 rule/ 保留进入观察期

Phase N 本身不执行目录删除。授权必须读取持久化 evidence bundle；当前主线仍为 NOT_EXECUTED。

## Phase O-R — Operational Closure Reconciliation

O-R 不是新的业务数据阶段，而是 N/O 的操作闭环补丁。

必须持久化：

- current_state
- cutover evidence
- observation evidence bundle
- 每次 run 的 run_id / snapshot_id / cutover commit SHA
- seven-client
- golden
- determinism
- artifact equivalence
- semantic regression
- source health

禁止使用手工 runs 数量作为证据。

## Phase O — Observation / Freeze / Retirement

至少观察 3 次真实、切换后的完整生产运行；每次都必须通过 seven-client、golden、determinism、artifact equivalence、semantic regression、source health。

只有观察期完成后才能进入 FROZEN_OLD_ROOT；退休仍需要人工批准，且任何脚本不得自动删除旧根。

## 最终状态

rule/ → transitional/frozen old root

rules/ → runtime Canonical Source of Truth

generated/ → generated client outputs only

database/services/ → 已删除的 Legacy Source
