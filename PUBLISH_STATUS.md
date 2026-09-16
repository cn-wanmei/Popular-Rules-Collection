# Publish & CI status

Repository: https://github.com/cn-wanmei/Popular-Rules-Collection

**Release lock:** [`docs/RELEASE_AND_QC.md`](docs/RELEASE_AND_QC.md)  
**Status:** 当前发布链路按 V3 Engine 运行；Collection、Build、Publish 均受 CI Gate 控制。机器生成区由 CI 自动刷新，人工备注仅保留于文末。

<!-- AUTO-GENERATED:BEGIN -->

## Automated status

由 `scripts/classify_health.py` 与 `scripts/generate_publish_status.py` 生成。不要手工编辑本区域。

### Authoritative inputs

- Source lifecycle: `sources/lifecycle.yaml`
- Raw health telemetry: `sources/health.yaml`
- Health policy: `config/health_policy.yaml`
- Retention policy: `config/retention.yaml`
- Client format registry: `config/formats.yaml`

### V3 pipeline

```
validate_registry / validate_dataset_registry / validate_ip_registry
  → collect / collection DAG
  → immutable snapshot
  → ingest → quarantine → canonical
  → hierarchy / decision → IR
  → adapters ×7
  → diff → golden → release gate
  → atomic promotion → generated/
```

### Source health

健康状态不再写入 `sources/health.yaml`；它只保存原始 telemetry。派生状态固定为：`healthy | degraded | stale | failed | retired`，由阈值策略自动计算并写入 `reports/source_health_status.yaml`。

### Retention

Retention 是独立维护流程，不属于 Collection 主 DAG。策略为 `config/retention.yaml`，执行器为 `scripts/retention.py`，工作流为 `.github/workflows/retention.yml`；默认 dry-run，破坏性清理必须显式 `workflow_dispatch` + `apply=true`。

### Legacy / V2

V2 migration layer、`scripts/normalize.py` 与旧兼容解析器已完成依赖扫描并删除。Git 历史保留作为审计记录；`scripts/legacy_reference_gate.py` 防止生产路径重新引入这些引用。

<!-- AUTO-GENERATED:END -->

## Human Notes

仅记录需要人工说明、但不应与机器状态混淆的例外事项。稳定运行状态、最近 Collection/Build/Publish、Source Health、客户端输出与 Retention 统计均由 CI 自动生成。

### Operational note

不要以单次 CI 失败直接判断已发布规则失效。当前生产状态应以 GitHub Actions、最近成功的 Collection/Build/Publish 及其 immutable evidence 为准。
