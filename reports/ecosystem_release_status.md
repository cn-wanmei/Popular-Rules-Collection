# Ecosystem Release Status (Read Model)

> **STALE OBSERVATION** — observed_at `2026-10-23T12:55:50Z`  

> Not SSOT. See `docs/STATE_MODEL.md`.


## Summary

| Field | Value |
|-------|-------|
| observation_status | **STALE OBSERVATION** |
| handoff_state | `COMPLETE` |
| collection_head | `bb1234dc3ea3bfea65e939070ff0092348d50e75` |
| source run / seal | `COMPLETE` / `COMPLETE` |
| icon semantic | `ok` |
| icon freeze | frozen=True freshness=`aging` |
| readability | `ok` |
| semantic_consistency | `ok` |

## Signal freshness

| Signal | freshness | age_seconds |
|--------|-----------|-------------|
| source_durable_bridge | stale | 1133743 |
| icon_identity_snapshot | aging | 562169 |

> ⚠️ **STALE OBSERVATION**: one or more underlying signals exceed hard SLA. Re-run Durable Bridge / Identity Freshness / Publish as appropriate.

