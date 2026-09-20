# Architecture

## Production Engine

src/engine/ 是 Service Rule 的唯一生产构建与运行路径。

~~~text
Source Registry
      ↓
Collection / Fetch
      ↓
Immutable Snapshot
      ↓
Ingest
      ↓
Quarantine
      ↓
Canonical
      ↓
Hierarchy + Decision
      ↓
Universal IR
      ↓
7 Client Adapters
      ↓
Diff + Golden
      ↓
Release Gate
      ↓
Atomic Promotion
      ↓
generated/
~~~

## Source Registry

Source Registry 是上游 Source 入口，不是 Canonical。

当前已登记 Supplemental Source：popular-rules-source。

入口状态：

~~~text
enabled = false
~~~

重新启用前必须证明 PRS official-evidence-only Release 已通过：

- Schema
- Evidence
- Ownership
- Boundary
- Exclusion
- Conflict
- Determinism
- Reconciliation

## Current Production State

当前 Service Production 仍为 partial。

P0 目标尚未达到 50/50；Phase O 的完整 cutover / observation 尚未执行。

因此：

- database/services/ 继续作为受控 Legacy 保留。
- rule/ 继续作为当前 V1 Canonical。
- generated/ 继续作为发布投影。
- data/runs/ 继续作为 immutable V3 evidence。

## Popular-Rules-Source Integration

启用后：

~~~text
Popular-Rules-Source
        ↓
Source Registry
        ↓
Collect
        ↓
V3 Engine
        ↓
7 Clients
~~~

PRS 不直接写 Collection Canonical、IR 或 generated client tree。

## Network Dataset

Network Dataset 与 Service Rule Runtime 分离：

~~~text
GeoIP / GeoSite / ASN / Provider / LAN
        ↓
Dataset Collectors
        ↓
database/*
        ↓
Dataset Validation
        ↓
Published Network Projections
~~~

## Architectural Invariant

~~~text
Source ≠ Canonical ≠ Runtime ≠ Generated
~~~
