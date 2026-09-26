# Google Sheets

> Current V3 service documentation. 本页记录当前 Service SSOT 身份，不等同于 Production 发布资格。

| 项目 | 内容 |
|------|------|
| Rule ID | `googlesheets` |
| Primary Ecosystem | `google` |
| Service Type | service |
| Parent Aggregate | `google` |
| Dedicated client outputs | 0 / 7 |
| Current State | candidate / review-required |

## 当前生产订阅路径

当前尚未在 generated/manifest.json 中物化独立生产客户端产物。

## 当前真源边界

- V3 Canonical：`data/runs/<run-id>/canonical/`
- Semantic IR：`data/runs/<run-id>/ir/`
- 最终发行：`generated/`
- `rule/`：V1 历史浏览/迁移树
- `rules/`：V3 目录契约
- Legacy evidence：`database/services/`，不是 V3 Runtime 真源

## Service Completion 状态

- Source 证据：已登记，等待当前 Source evidence gate
- Source immutable release：PENDING
- Collection exact binding：PENDING
- Semantic / overlap audit：PENDING
- Seven-client：PENDING
- Golden：PENDING
- Canary：PENDING
- Production：PENDING

> Candidate / Source release 不等于 Production；生产资格必须由 immutable provenance 与现有硬门决定。
