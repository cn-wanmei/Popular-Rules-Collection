# Phase J — Third-round audit remediation

> Tracker only. P0 in audit: **0**.

## Durable Bridge #77

| Run | Result | Cause |
|-----|--------|-------|
| #77 | failure | selective `services=12306` — **unknown service** (not in Source registry) |
| #78 | success | `services=netflix` (valid batch id) |
| follow-up | fixed empty `executed_services` (pre-merge run snapshot) |

**Not a residual syntax bug.** Selective input must use real Source service ids.

## Completed

| ID | Item |
|----|------|
| P1-01 | Content-based identity drift |
| P1-02/03 | planned/executed + lock; run snapshot fix |
| P1-04 | `handoff_state` in Read Model |
| P1-05 | `observation_status` + status markdown STALE markers |
| P2-01 | STATE_MODEL schema alignment |
| P2-02 | Raw E2E sha256/size |
| P2-03 | Recovery Sandbox LKG digest job |
| P2-04 | Plan requirements.lock |
| P2-05 | Icon freeze TTL fields |

## Operator notes

- Durable selective: ids from `config/durable_release_policy.yaml` / Source registry only.
- Freeze expiry is policy metadata; promotion still requires human review.
