# Funnel triage (Source degraded + REVIEW pool)

> **Historical observation snapshot (P1-02 / docs cleanup 2026-10-09).**  
> Live Source health counts: [`reports/source_health_status.yaml`](../reports/source_health_status.yaml)  
> Live publish status: [`PUBLISH_STATUS.md`](../PUBLISH_STATUS.md)  
> Live ecosystem read-model: [`reports/ecosystem_release_status.json`](../reports/ecosystem_release_status.json)  
> Do not treat embedded tables below as current production health.


Companion to `FUNNEL_OPS.md` and Source `FUNNEL_ACCELERATION.md`.

## Collection Source health counts

`PUBLISH_STATUS.md` **Source health** comes from Collection `sources/health.yaml` + `sources/lifecycle.yaml` via `classify_health.py` — **not** the full Source repo service list (~282).

## Snapshot post-Collect 2026-10-08 (`reports/source_health_status.yaml` ~05:36Z)

| Source id | Status | Notes |
|-----------|--------|--------|
| lm-firefly | **healthy** | recovered after Collect |
| blackmatrix7, dler, metacubex, popular-rules-source, v2fly | healthy | |
| anti-ad, hagezi, loyalsoldier, sukkaw | **stale** | last success ~2026-10-01; age ~169h |

### Operator actions

1. Stale quartet: verify registry fetch paths / upstream availability; do not clear LKG empty.
2. Collect run `37732034677` completed **success**.
3. Never clear LKG with empty body.

## REVIEW pool (Source lifecycle)

- Large REVIEW is normal until evidence complete.
- Weekly ≥8 VERIFIED→CANARY when ready.
- `cloudflare`: domains=0 / BLOCKED — keep blocked until adapter/policy fix.

Do **not** bulk-edit `source_canary_state.yaml` without per-service evidence.
