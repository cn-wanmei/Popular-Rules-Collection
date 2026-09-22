# Architecture — Current V3

```text
upstream → Collect → immutable backup → V3 Engine
→ Canonical → Semantic IR → 7 Client Adapters
→ Network Dataset Materialization → deterministic RC → atomic publish → generated/
```

| Layer | Role |
|---|---|
| `backup/<date>` | immutable input |
| `data/runs/<run>/canonical` | V3 Canonical truth |
| `data/runs/<run>/ir` | Semantic IR |
| `generated/<client>` | client distribution |
| `generated/<network-scope>` | Network Dataset |
| `rule/` | V1 legacy browse/migration |
| `rules/` | V3 directory contract |

Popular-Rules-Source is upstream Evidence Supply; Collection consumes it through immutable Source lineage binding。