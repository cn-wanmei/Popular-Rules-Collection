# Universal Rules Data Platform

> 下一代多生态网络规则数据供应链

当前仓库进入 V1 架构重建阶段。原项目的采集、不可变快照、统一语义、多客户端 Adapter、质量验证思想继续继承，但旧 V2/V3/legacy 路径不会继续扩张。

## 核心目标

这不是规则文件仓库，而是一个可验证、可审计、可复现、可回滚的规则数据供应链：

```text
Source Registry
  → Collector
  → Immutable Snapshot
  → Parser
  → Canonical Model
  → Deduplicate / Conflict / Coverage
  → Decision
  → Semantic IR
  → Client Adapter
  → Semantic Verification
  → Release Gate
  → Immutable Release
```

## 架构不变量

- Git 只保存代码、配置、Schema、Tests、Decision、Docs。
- Snapshot / CAS / Run / Report / Release Artifact 不进入 Git 运行时状态。
- Builder 必须离线，只消费 Snapshot Manifest。
- Source 失败或异常不得覆盖生产数据；使用 quarantine + last-known-good。
- Parser 不做业务决策；Adapter 不改变规则逻辑。
- 所有规范化、排序、构建和发布均必须 deterministic。
- semantic loss 必须显式暴露，不得为了客户端覆盖率伪造规则。

## 当前阶段

**Phase 0：架构冻结。** 已建立：

- `docs/PLATFORM_V1_ARCHITECTURE.md`
- `docs/ADR-0001-platform-foundation.md`
- `schemas/source.schema.json`
- `schemas/rule.schema.json`
- `schemas/decision.schema.json`
- `schemas/ir.schema.json`
- `schemas/release.schema.json`
- `config/platform-sources.yaml`
- `config/clients.yaml`
- `decisions/README.yaml`

下一阶段先实现最小闭环：HTTP Source → Snapshot → Parser → Canonical → Mihomo → Validation → Release；在闭环稳定前不扩展七客户端。

## 旧系统迁移原则

`main` 当前生产链保持独立。V1 通过 `platform-v1` 分支逐步建立新边界；任何 legacy 数据只有在完成 lineage、schema、reproducibility 与 migration tests 后才允许迁移。

## License

MIT
