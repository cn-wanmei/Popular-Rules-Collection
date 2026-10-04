# Phase J — Third-round audit (语义精修)

> Tracker only. Audit date 2026-10-04. P0 count in audit: **0**.

## CI (main tip)

| Repo | Status |
|------|--------|
| Collection | green (Build/Publish/Raw E2E/Recovery) |
| Source | CI #511 green; #512 `action_required` is PR approval noise (0 jobs) |
| Icon | Identity Freshness #7 green after snapshot merge |

## Completed this cycle

| ID | Item |
|----|------|
| P1-01 | Identity drift = content (`file_sha` / ids / fields); HEAD-only move ≠ drift |
| P1-02/03 | Durable `planned_services` + `missing_from_execution`; plan uses `requirements.lock` |
| P1-02 runtime | Selective Durable dispatch (`services=12306`) for new workflow evidence |
| P2-01 | STATE_MODEL → `ecosystem_release_status_v3` |
| P2-02 | Raw E2E manifest sha256/size vs body |
| P2-04 | Plan job lock discipline |

## Deferred

| ID | Item |
|----|------|
| P1-04 | Unified handoff_state in Read Model (COMPLETE / MANUAL_ACTION_REQUIRED) |
| P1-05 | Stronger STALE OBSERVATION UI in status MD |
| P2-03 | Recovery Sandbox Drill |
| P2-05 | Icon freeze TTL |
| P2-06 | README vs manifest role further split |
