# Architecture — Current V3

> 当前架构与 [ARCHITECTURE.md](ARCHITECTURE.md) 保持一致；本文件作为兼容入口。

```text
Upstream
  ↓
Collect → immutable backup/<date>
  ↓
V3 Engine
  ↓
Canonical → Semantic IR
  ├── rule/               人类浏览 / 服务选择
  └── generated/          客户端 + Network Dataset
  ↓
Deterministic Release Candidate → Atomic Publish
```

当前规则总索引是 `rule/_index.yaml`，客户端最终文件清单是 `generated/manifest.json`；不存在当前使用的 `rule/manifest.json`。