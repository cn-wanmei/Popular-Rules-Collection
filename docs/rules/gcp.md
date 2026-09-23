# Google Cloud Platform (GCP)

> Current V3 service documentation. GCP currently remains an alias-boundary review against Google Cloud and is not materialized as a duplicate production Source snapshot.

| 项目 | 内容 |
|------|------|
| Rule ID | `gcp` |
| Primary Ecosystem | `google` |
| Service Type | service |
| Parent Aggregate | `google` |
| Release Date | — |
| Dedicated client outputs | 0 / 7 |

## 当前生产订阅路径

当前 GCP 条目处于 alias-boundary review。其候选证据与 Google Cloud 的 canonical service surface 重叠，因此当前不生成重复的 immutable production binding。

## 当前真源边界

- GCP Candidate：`Popular-Rules-Source/authoring/candidates/gcp.jsonl`
- Google Cloud Source：`Popular-Rules-Source/generated/source/googlecloud/`
- V3 Canonical：`data/runs/<run-id>/canonical/`
- Semantic IR：`data/runs/<run-id>/ir/`
- 最终发行：`generated/`

## 维护规则

在 GCP 与 Google Cloud 的边界获得独立证据前，不得把两个服务的相同域集合分别复制进入 production。

---
_页面日期来源：2026-09-23。_
