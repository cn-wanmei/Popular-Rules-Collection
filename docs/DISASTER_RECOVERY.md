# Disaster Recovery Runbook

> **Status: Current**  
> Unified recovery entry. Per-repo details remain in local runbooks; this file is the cross-repo map.

## Principles

1. **SSOT stays in place** — do not invent a fourth authority during incidents.
2. **Last Known Good** over “latest at all costs”.
3. **Fail closed** — missing evidence / invalid candidate → freeze, do not force publish.
4. **Remediation must be visible** — branch, PR, or sealed report; no silent success.

## Authority map

| Concern | Authority |
|---------|-----------|
| Evidence / durable seal | Source (`releases/`, `snapshots/`, `reports/durable-bridge/latest.json`) |
| Canonical identity / rules / publish | Collection (`rule/_index.yaml`, `PUBLISH_STATUS.md`) |
| Icon assets / production pointer | Icon (`config/release-pointers.yaml`, `dist/`) |
| Cross-repo overview | Read model only: `reports/ecosystem_release_status.json` |

## Scenario matrix

### S1 — Source durable artifact missing / incomplete

| Step | Action |
|------|--------|
| Detect | `reports/durable-bridge/latest.json` → `batch_completeness` PARTIAL/FAILED; CI Durable Bridge red |
| Freeze | Do not open Collection handoff for affected services |
| Recover | Re-run `durable-source-bridge.yml` (selective `services=` if needed); confirm PERSISTED + digests |
| Verify | `batch_completeness` COMPLETE or explicit PARTIAL with known incomplete list |
| Unlock | Resume Collection Auto Handoff only for sealed services |

### S2 — Collection publish candidate invalid

| Step | Action |
|------|--------|
| Detect | Build / Publish fail-closed gates; Publish status degraded |
| Freeze | Do not promote RC; keep previous public `main` trees |
| Recover | Fix candidate; re-run Build → Publish with exact artifact identity |
| Verify | Publish success; Published Raw E2E green |
| Unlock | Consumers continue on last good public raw |

### S3 — Public Raw 404 / empty

| Step | Action |
|------|--------|
| Detect | `Published Raw E2E` fail-closed HTTP ≠ 200 |
| Freeze | Treat public surface as degraded; investigate last Publish |
| Recover | Re-Publish last known good RC if available; or repair tree on `main` via controlled Publish path |
| Verify | Raw E2E PASS (7 clients + leaf samples) |

### S4 — Icon identity drift

| Step | Action |
|------|--------|
| Detect | Identity Freshness report `drift: true` |
| Freeze | Do not cut Icon production release on stale snapshot |
| Recover | Allow automation PR from Freshness; review + merge snapshot refresh |
| Verify | Freshness NO DRIFT; snapshot `source.ref` = exact Collection SHA + `file_sha` |
| Unlock | Proceed with Icon release pipeline |

### S5 — Icon production pointer wrong

| Step | Action |
|------|--------|
| Detect | Operator / consumer report; pointer vs dist mismatch |
| Freeze | Stop promoting new pointer |
| Recover | Point `config/release-pointers.yaml` to last known good release id; follow Icon rollback runbook |
| Verify | Pointer resolves; gallery/sample fetch OK |

### S6 — Source canary SSOT corruption

| Step | Action |
|------|--------|
| Detect | Lifecycle status anomaly; canary state parse failure |
| Freeze | Block canary promotions |
| Recover | `restore-canary-state.yml` / known-good commit of `config/source_canary_state.yaml` |
| Verify | Lifecycle report coherent; Source CI green |

## Common command surfaces

```text
Source:   Actions → Durable Source Bridge / CI / restore-canary-state
Collection: Actions → Build Client Rules / Publish Release Candidate / Published Raw E2E
Icon:     Actions → Identity Freshness / PR CI (L0–L1)
Read model: Actions → Ecosystem Status (Read Model)
```

## Related

- Collection `docs/RELEASE_RUNBOOK.md`
- Collection `docs/STATE_MODEL.md`
- Source `docs/CI_AUTOMATION.md`
- Icon `docs/IDENTITY_BOUNDARY_V1.md`
- `docs/PHASE_H_PROGRESS.md`
