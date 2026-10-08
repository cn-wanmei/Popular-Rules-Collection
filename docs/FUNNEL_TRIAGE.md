# Funnel triage (Source degraded + REVIEW pool)

Companion to `FUNNEL_OPS.md` and Source `FUNNEL_ACCELERATION.md`.

## Collection Source health counts

`PUBLISH_STATUS.md` **Source health** is derived from Collection `sources/health.yaml` + `sources/lifecycle.yaml` via `classify_health.py` — **not** the full Source repo service list (~282).

Typical small counts (e.g. degraded 4 / healthy 6) mean **telemetry-covered Collection sources**, not global Source lifecycle histogram.

## Degraded playbook (P0 ops)

1. Inspect `reports/source_health_status.yaml` for ids with `status: degraded|failed|stale`.
2. On Source: `python -m source_engine gap --service <id>` then `repair` if appropriate.
3. Never overwrite LKG with empty fetch.
4. Permanent upstream loss → Source `BLOCKED` / tombstone + Collection lifecycle note.

## REVIEW pool (Source lifecycle)

From Source README summary (CI-generated):

- Large **REVIEW** count is expected until evidence complete.
- Weekly: ≥8 `VERIFIED → CANARY` when candidates ready.
- Long REVIEW without official evidence → BLOCKED or remove from active qualify queue.

Do **not** bulk-edit `source_canary_state.yaml` without per-service evidence.
