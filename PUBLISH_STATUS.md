# Publish & CI status

Repository: https://github.com/cn-wanmei/Popular-Rules-Collection

**Release lock:** [`docs/RELEASE_AND_QC.md`](docs/RELEASE_AND_QC.md)  
**Status:** 当前发布链路按 V3 Engine 运行；Collection、Build、Publish 均受 CI Gate 控制。机器生成区由 CI 自动刷新，人工备注仅保留于文末。
<!-- AUTO-GENERATED:BEGIN -->
## Automated status

Generated at: `2026-10-09T17:25:19.913356Z`

### Collection
- Latest snapshot date: `2026-10-09`
- Collection ID: `2026-10-09-6a5edf0e7f5021c856e9`
- Status: `ok`
- Root: `backup/2026-10-09`

### Source health
- Scope: Collection `sources/health.yaml` telemetry (10 sources); **not** full Source repo lifecycle count
- Details: `reports/source_health_status.yaml` · triage: `docs/FUNNEL_TRIAGE.md`
- `healthy`: 6
- `retired`: 4

### Generated clients
- egern: `generated/egern`
- loon: `generated/loon`
- mihomo: `generated/mihomo`
- quantumultx: `generated/quantumultx`
- shadowrocket: `generated/shadowrocket`
- singbox: `generated/singbox`
- surge: `generated/surge`


### Retention
- Policy: `config/retention.yaml`
- Backup keep_days: `30`
- Release evidence keep_days: `180`
- Workflow: `.github/workflows/retention.yml` (weekly dry-run)

<!-- AUTO-GENERATED:END -->
## Human Notes

仅记录需要人工说明、但不应与机器状态混淆的例外事项。稳定运行状态、最近 Collection/Build/Publish、Source Health、客户端输出与 Retention 统计均由 CI 自动生成。

### Operational note

不要以单次 CI 失败直接判断已发布规则失效。当前生产状态应以 GitHub Actions、最近成功的 Collection/Build/Publish 及其 immutable evidence 为准。

### Source health scope

`degraded` / `healthy` 计数来自 **本仓** `sources/health.yaml`（Collect telemetry），不是 Source 仓全量 lifecycle（见 Source README 摘要与 `reports/generated/lifecycle.json`）。分诊：[`docs/FUNNEL_TRIAGE.md`](docs/FUNNEL_TRIAGE.md)。

### Icon pointer

Collection pins must match Icon `release-pointers.yaml`. Gate: `python scripts/check_icon_pointers.py`. Sync runbook: [`docs/ICON_POINTER_SYNC.md`](docs/ICON_POINTER_SYNC.md).
