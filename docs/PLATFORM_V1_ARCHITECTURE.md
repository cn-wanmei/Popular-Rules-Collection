# Universal Rules Data Platform

> 下一代多生态网络规则数据供应链

## 架构冻结声明

本分支用于 Universal Rules Data Platform V1 的架构重建。旧 V2/V3/legacy 运行路径不得成为新系统依赖；迁移只能通过明确的 Snapshot/Canonical/Decision/IR 边界进行。

## SSOT

唯一规则语义真相源：Canonical Rule Database / Semantic IR。

Git 仅保存代码、配置、Schema、Tests、Decision 与文档；运行时 Snapshot、CAS、Run、Report、Release Artifact 不进入 Git。

## Pipeline

```text
Registry → Collect → Immutable Snapshot → Parse → Canonicalize
→ Analyze(Dedupe/Conflict/Coverage) → Decision → Semantic IR
→ Adapter → Semantic Verify → Release Gate → Immutable Release
```

## 不变量

1. Builder 离线运行，不访问 Internet。
2. Source failure 不得产生空规则覆盖；异常进入 quarantine，并优先使用 last-known-good。
3. Parser 不做业务决策；Adapter 不修改规则逻辑。
4. 所有规范化、排序、构建、发布结果必须 deterministic。
5. Release 必须携带完整 lineage、hash、engine/schema/decision/snapshot 信息。
6. Semantic loss 必须显式报告，不得为了客户端覆盖率伪造等价规则。

## Phase 0

当前只冻结：Source / Snapshot / Rule / Decision / IR / Release 数据边界，以及客户端 capability matrix。暂不迁移全部生产数据，也暂不实现七客户端 Adapter。