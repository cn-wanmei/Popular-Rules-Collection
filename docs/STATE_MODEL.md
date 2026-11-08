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
| fresh | verified against authority within SLA (e.g. ≤ 24h soft / 7d hard for read-model labels) |
| aging | within 2× soft SLA |
| stale | beyond hard SLA or explicit content drift |
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

## Icon identity freshness evidence

The Icon identity snapshot is content-addressed and intentionally remains unchanged when Collection's `rule/_index.yaml` identity content does not change. Its `generated_at` records snapshot generation, not a verification heartbeat.

The cross-repo read model therefore uses the latest completed successful Icon **Identity Freshness** workflow artifact as the verification clock. It is fresh only when the report is within the hard SLA, `drift=false`, `content_match=true`, live and pinned SHA-256 values match the currently observed Collection index and Icon snapshot, and there are no missing IDs, extra IDs, or field mismatches. Snapshot age remains visible as informational metadata. Missing reports, stale runs, hash mismatches, drift, or semantic warnings fail closed.

This is stronger than comparing service counts alone and preserves the content-based rule that a Collection HEAD move without an index-content change does not require rewriting the Icon snapshot.

## Anti-patterns

- Encoding freshness into the lifecycle field
- Treating “service count match” as freshness proof (Icon snapshot)
- Treating snapshot `generated_at` as a heartbeat when the snapshot is immutable
- Treating Collection HEAD move alone as identity drift when `rule/_index.yaml` file_sha is unchanged
- Creating a fifth authoritative status file that re-owns lifecycle

## Cross-repo read model

Generated aggregate (non-authoritative):

```text
reports/ecosystem_release_status.json
schema: ecosystem_release_status_v3
```

Fields of note:

| Field | Meaning |
|-------|--------|
| `observed_at` / `observation_watermark` | When the observation was taken |
| `readability` | Signals could be fetched |
| `semantic_consistency` | Cross-repo content checks (e.g. Collection index file_sha vs Icon pin) |
| `freshness` | Age labels on individual signals |

Historical schema names (`v1`, `v2`) are superseded; do not treat them as current contract.
