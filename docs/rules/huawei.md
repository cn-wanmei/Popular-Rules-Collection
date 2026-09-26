# Huawei

> Current V3 service documentation. 本页记录当前 Service SSOT 身份，不等同于 Production 发布资格。

| 项目 | 内容 |
|------|------|
| Rule ID | `huawei` |
| Primary Ecosystem | `huawei` |
| Service Type | aggregate |
| Parent Aggregate | — |
| Dedicated client outputs | 7 / 7 |
| Current State | candidate / review-required |

## 当前生产订阅路径

- `egern/huawei/huawei/huawei.yaml`
- `loon/huawei/huawei/huawei.list`
- `mihomo/huawei/huawei/huawei.yaml`
- `quantumultx/huawei/huawei/huawei.list`
- `shadowrocket/huawei/huawei/huawei.list`
- `singbox/huawei/huawei/huawei.json`
- `surge/huawei/huawei/huawei.list`

## 当前真源边界

- V3 Canonical：`data/runs/<run-id>/canonical/`
- Semantic IR：`data/runs/<run-id>/ir/`
- 最终发行：`generated/`
- `rule/`：V1 历史浏览/迁移树
- `rules/`：V3 目录契约
- Legacy evidence：`database/services/`，不是 V3 Runtime 真源

## Service Completion 状态

- Source 证据：按当前 Source evidence gate 验证
- Source immutable release：PENDING
- Collection exact binding：PENDING
- Semantic / overlap audit：PENDING
- Seven-client：当前 manifest 已有产物
- Golden：PENDING
- Canary：PENDING
- Production：PENDING

> Candidate / Source release 不等于 Production；生产资格必须由 immutable provenance 与现有硬门决定。
