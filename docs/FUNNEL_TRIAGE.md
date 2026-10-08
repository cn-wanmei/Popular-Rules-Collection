# Funnel triage (Source degraded + REVIEW pool)

Companion to `FUNNEL_OPS.md` and Source `FUNNEL_ACCELERATION.md`.

## Collection Source health counts

`PUBLISH_STATUS.md` **Source health** comes from Collection `sources/health.yaml` + `sources/lifecycle.yaml` via `classify_health.py` — **not** the full Source repo service list (~282).

## Snapshot 2026-10-08 (`reports/source_health_status.yaml`)

| Source id | Status | Notes |
|-----------|--------|--------|
| anti-ad | **degraded** | last success ~166h |
| hagezi | **degraded** | last success ~166h |
| loyalsoldier | **degraded** | last success ~166h |
| sukkaw | **degraded** | last success ~166h |
| lm-firefly | **failed** | `failure_count>0`; fetch `Apple/AppleDev.list` from `LM-Firefly/Rules@master` |
| blackmatrix7, dler, metacubex, popular-rules-source, v2fly | healthy | recent success |

### Operator actions

1. **Collect Upstream** manually dispatched 2026-10-08 (~run `37732034677`) to refresh degraded sources if upstream reachable.
2. **lm-firefly**: registry `sources/registry.yaml` id `lm-firefly` → `github_raw` `LM-Firefly/Rules` path `Apple/AppleDev.list`. On persistent fail: check upstream file move/404; do not clear LKG with empty body.
3. Never clear LKG with empty body.

## REVIEW pool (Source lifecycle)

- Large REVIEW is normal until evidence complete.
- Weekly ≥8 VERIFIED→CANARY when ready.
- `cloudflare`: domains=0 / BLOCKED — keep blocked until adapter/policy fix (Source `BLOCKED_BOARD`).

Do **not** bulk-edit `source_canary_state.yaml` without per-service evidence.
