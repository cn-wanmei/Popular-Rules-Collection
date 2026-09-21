# Publish & CI status

Repository: https://github.com/cn-wanmei/Popular-Rules-Collection

**Release lock:** [`docs/RELEASE_AND_QC.md`](docs/RELEASE_AND_QC.md)  
**Status:** 当前发布链路按 V3 Engine 运行；Collection、Build、Publish 均受 CI Gate 控制。机器生成区由 CI 自动刷新，人工备注仅保留于文末。
<!-- AUTO-GENERATED:BEGIN -->
## Automated status

Generated at: `2026-09-21T04:42:23.694783Z`

### Collection
- Latest snapshot date: `2026-09-21`
- Collection ID: `2026-09-21-995e7fc3c49be580cc83`
- Status: `ok`
- Root: `backup/2026-09-21`

### Source health
- `healthy`: 6
- `stale`: 4

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

<!-- AUTO-GENERATED:END -->
## Human Notes

仅记录需要人工说明、但不应与机器状态混淆的例外事项。稳定运行状态、最近 Collection/Build/Publish、Source Health、客户端输出与 Retention 统计均由 CI 自动生成。

### Operational note

不要以单次 CI 失败直接判断已发布规则失效。当前生产状态应以 GitHub Actions、最近成功的 Collection/Build/Publish 及其 immutable evidence 为准。
