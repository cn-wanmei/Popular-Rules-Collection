# Phase G — Governance & Convergence (progress)

> **Status: Current operational tracker**  
> Not a SSOT. Production numbers remain in `PUBLISH_STATUS.md` / Source lifecycle / Icon pointers.

## CI verification (2026-10-03, token-confirmed)

| Check | Result |
|-------|--------|
| Collection Unit Tests | **success** #1925 |
| Collection Engine v3 | **success** #1234 |
| Collection Architecture Gate (Build #830) | **success** |
| Collection Published Raw E2E | **success** #1 |
| Collection Ecosystem Status | **success** #1 |
| Icon Identity Freshness | **success** #4 (workflow_dispatch) |
| Source CI | **success** #506 |

Root cause of prior reds: `ecosystem-status.yml` / `published-raw-e2e.yml` violated `architecture_gate` (workflow-level permissions). Fixed on `8295d80`.

## Completed

| ID | Item |
|----|------|
| G1a/b | Workflow classification + inventory |
| G1c-doc | Recommended required checks documented in WORKFLOWS.md |
| G2 | Source security contract / lock / SHA pins |
| G3 | Icon identity freshness + false-drift fix + soft sync-pr |
| G4a–c | Pipeline / Identity Final / historical index |
| G4d | RISK/R14 marked Historical banners |
| G5 | Durable selective matrix + policy |
| G6 | Cross-repo read model |
| G7 | Four-dimension state model |
| G8 | Published Raw E2E |
| G | Root SECURITY.md (Collection + Icon); Source SECURITY updated |

## Remaining (optional / settings)

| ID | Item | Notes |
|----|------|--------|
| G1c-settings | Branch protection required status checks | Collection/Source main protection exists but **no required checks configured**; Icon main **unprotected**. Configure in repo Settings (or admin API) — do not force without reviewing current rules. |
| G4d-move | Physical `docs/archive/` path move | Banners applied; optional path migration |

## Non-goals

- No additional authoritative status databases
- No new gate workflows without retiring duplicates
- No handwritten coverage counts in README
