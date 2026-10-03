# Phase I — Third-round audit remediation

> Tracker only — not SSOT. Audit: 2026-10-04 reverse cross-check.

## P0

| ID | Item | Status |
|----|------|--------|
| P0-01 | Raw E2E real `generated/` contract (`singbox`, manifest, 7 client leaves) | **done** |
| P0-02 | Icon snapshot pinned to Collection `7906b939…` + live `file_sha` | **done** |

## P1

| ID | Item | Status |
|----|------|--------|
| P1-01 | Durable `run_completeness` / `seal_completeness` | **done** |
| P1-02 | Durable least privilege (write only persist) | **done** |
| P1-03 | Durable concurrency + fail-closed git | **done** |
| P1-04 | Read Model Collection↔Icon SHA/file_sha | **done** |
| P1-05 | Read Model age / freshness labels | **done** |
| P1-06 | Icon Freshness daily + `repository_dispatch` | **done** |
| P1-07 | Icon release build-and-gate `contents: read` | **done** |
| P1-08 | Source generate handoff not soft-success | **done** |

## P2 (deferred)

| ID | Item |
|----|------|
| P2-01 | True restore/rebuild Recovery Drill |
| P2-02 | Per-client leaf matrix already improved via manifest |
| P2-03 | Source README lifecycle slim |
| P2-04 | Unified cross-repo freshness SLA automation |
