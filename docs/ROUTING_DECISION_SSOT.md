# Routing Decision SSOT

## 原则

- **Semantic uniqueness**：同一 domain 最终 `action` 唯一（DIRECT|PROXY|REJECT）
- **Textual multiplicity**：客户端可展开多种 rule 形态
- **SSOT**：`generated/routing/decisions.jsonl`
- **派生物**：`direct.list` / `proxy.list` / `reject.list` / `conflicts.json`
- **Provenance**：`decisions.meta.json`（`decision_digest`）

```bash
python scripts/routing_emit.py
```

Builders 应迁移消费 decision 派生物；过渡期 service 产物仍可由 `rule_loader` 生成。
