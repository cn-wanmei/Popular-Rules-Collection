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
| lm-firefly | **failed** | failure_count > 0 |
| blackmatrix7, dler, metacubex, popular-rules-source, v2fly | healthy | recent success |

### Operator actions

1. Next **Collect Upstream** should refresh anti-ad / hagezi / loyalsoldier / sukkaw if upstream reachable.
2. Investigate **lm-firefly** adapter/URL (failure_count positive).
3. Never clear LKG with empty body.

## REVIEW pool (Source lifecycle)

- Large REVIEW is normal until evidence complete.
- Weekly ≥8 VERIFIED→CANARY when ready.
- `cloudflare`: domains=0 / BLOCKED — keep blocked until adapter/policy fix (Source `BLOCKED_BOARD`).

Do **not** bulk-edit `source_canary_state.yaml` without per-service evidence.
