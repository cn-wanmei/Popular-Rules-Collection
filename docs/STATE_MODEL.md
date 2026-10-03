# State Model — Lifecycle × Freshness × Health × Lineage

> **Status: Current contract**  
> Dimensions are **orthogonal**. A service can be `lifecycle=production` and still `freshness=stale`.
>
> This document defines vocabulary only. Authoritative values remain in each repo SSOT.

## Four dimensions

| Dimension | Question | Typical SSOT |
|-----------|----------|--------------|
| **Lifecycle** | Where is this service in the promotion machine? | Source / Collection `source_canary_state` |
| **Freshness** | How current is the consumed artifact vs upstream authority? | Snapshot age, Icon identity snapshot, binding digest age |
| **Health** | Can upstream / pipeline be relied on right now? | Source health reports, collect status |
| **Lineage** | Is the immutable chain intact (snapshot → release → binding)? | Immutable registry, durable bridge, publish identity |

## Allowed values (normative vocabulary)

### Lifecycle

```text
review → verified → canary → production
(+ blocked as policy hold)
```

### Freshness

```text
fresh | aging | stale | unknown
```

Policy example (operators may tighten):

| Label | Example rule of thumb |
|-------|------------------------|
| fresh | verified against authority within SLA (e.g. ≤ 7d) |
| aging | within 2× SLA |
| stale | beyond 2× SLA or explicit drift detected |
| unknown | no last_verified_at |

### Health

```text
healthy | degraded | blocked | unknown
```

### Lineage

```text
valid | incomplete | broken | unknown
```

## Examples

| Lifecycle | Freshness | Health | Lineage | Operator reading |
|-----------|-----------|--------|---------|------------------|
| production | fresh | healthy | valid | Steady state |
| production | stale | healthy | valid | Re-run durable / handoff; do not “un-produce” blindly |
| canary | fresh | degraded | valid | Hold promotion; fix upstream |
| verified | fresh | healthy | incomplete | Missing durable seal |

## Anti-patterns

- Encoding freshness into the lifecycle field
- Treating “service count match” as freshness proof (Icon snapshot)
- Creating a fifth authoritative status file that re-owns lifecycle

## Cross-repo read model

Generated aggregate (non-authoritative): `reports/ecosystem_release_status.json` (schema `ecosystem_release_status_v1`).
