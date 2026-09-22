# Architecture — Current V3

```text
upstream → Collect → immutable backup
→ Canonical → Semantic IR
→ ├─ human Rule Browse Distribution → rule/
  └─ Client / Network Distributions → generated/
→ deterministic RC → atomic Git publish
```

| Layer | Role |
|---|---|
| `sources/` | upstream source definitions |
| `backup/<date>` | immutable input |
| `data/runs/<run>/canonical` | **V3 Canonical truth** |
| `data/runs/<run>/ir` | **Semantic IR** |
| `rule/` | **human browsing / search / selection distribution** |
| `generated/<client>` | **client rule distribution** |
| `generated/<network>` | **network dataset distribution** |
| `docs/` | architecture, usage and audit documentation |
| `rules/` | **deleted; never recreate as a third rule tree** |

`rule/` and `generated/` are sibling projections of one immutable Run. The human tree is built from Semantic IR, not copied back from a client adapter.

## Release invariant

`rule/manifest.json` and `generated/manifest.json` are bound to the same Run and Semantic IR digest. Publish and rollback replace both projections together.

Popular-Rules-Source remains the upstream evidence supply; Collection consumes it through immutable Source lineage.