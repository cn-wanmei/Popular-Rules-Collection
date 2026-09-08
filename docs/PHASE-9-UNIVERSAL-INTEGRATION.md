# Phase 9 — Universal-Rules-Collection 接入

## 目标

将 `Universal-Rules-Collection` 的 stable `client-input` 作为本仓库的上游标准规则输入，同时保持现有 V3 Engine、7 客户端 adapters 与发布门禁不被旁路破坏。

## 上游唯一入口

配置：`config/upstream/universal-rules.yaml`

- manifest：用于 release identity、rule count、checksum
- client-input：Canonical Rule JSONL
- schema：Canonical Rule Schema

## Fail-closed

同步器必须验证：

1. SHA-256 checksum 与 manifest 完全一致。
2. 实际规则数量与 manifest 一致。
3. 每条规则包含 id/kind/pattern/action/source/sources/provenance/category/popularity_score。
4. action 不得为 UNKNOWN。
5. provenance 不得为空。

任一条件失败都不得更新 `data/upstream/universal/`。

## 数据边界

```text
Universal-Rules-Collection
  → stable/client-input.jsonl
  → sync_universal.py
  → data/upstream/universal/
  → V3 Engine / hierarchy / decision / IR
  → adapters × 7
  → generated/
```

Universal 负责**规则事实、Canonical IR、分类与稳定性**；Popular 负责**客户端能力、服务层决策、格式适配和最终发布**。

## 当前状态

Phase 9 首批落地的是“可信上游接入层”，不会把 Universal 数据直接覆盖现有生产数据。这样可以先完成 checksum/provenance/数量门禁，再逐步把 Universal category 与 popularity_score 接入 V3 hierarchy/decision。
