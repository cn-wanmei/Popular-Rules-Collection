# Phase G — Governance & Convergence (progress)

> **Status: Current operational tracker**  
> Not a SSOT. Production numbers remain in `PUBLISH_STATUS.md` / Source lifecycle / Icon pointers.

## CI verification (2026-10-03)

| Check | Result |
|-------|--------|
| Collection Unit Tests | **success** #1925 |
| Collection Engine v3 | **success** #1234 |
| Collection Architecture Gate (Build #830) | **success** |
| Collection Published Raw E2E | **success** #1 |
| Collection Ecosystem Status | **success** #1 |
| Icon Identity Freshness | **success** #4 |
| Source CI | **success** #506 |

Prior reds: `ecosystem-status` / `published-raw-e2e` violated `architecture_gate` (workflow-level permissions) → fixed on `8295d80`.

## Completed

| ID | Item |
|----|------|
| G1a/b | Workflow classification + inventory |
| G1c | `docs/BRANCH_PROTECTION.md` + link from WORKFLOWS |
| G2 | Source security contract / lock / SHA pins |
| G3 | Icon identity freshness + false-drift fix |
| G4a–c | Pipeline / Identity Final / historical index |
| G4d | RISK/R14 → stubs + `docs/archive/status/` + immutable history `5c359c5` |
| G5 | Durable selective matrix + policy |
| G6 | Cross-repo read model |
| G7 | Four-dimension state model |
| G8 | Published Raw E2E |
| G | SECURITY.md across repos |

## Operator-only remainder

| ID | Item | Action |
|----|------|--------|
| G1c-UI | Turn on required checks in GitHub Settings | Follow `docs/BRANCH_PROTECTION.md` (API not force-applied) |
| Build #830 | Long production steps may still run | Architecture Gate already **success** |

## Non-goals

- No additional authoritative status databases
- No new gate workflows without retiring duplicates
- No handwritten coverage counts in README
