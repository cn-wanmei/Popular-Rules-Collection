# Phase G — Governance & Convergence (progress)

> **Status: Current operational tracker**  
> Not a SSOT. Production numbers remain in `PUBLISH_STATUS.md` / Source lifecycle / Icon pointers.

Audit basis: 2026-10-03 cross-repo audit (Architecture ready → Governance focus).

## Completed

| ID | Item | Where |
|----|------|--------|
| G1a | Workflow classification index | `docs/WORKFLOWS.md` |
| G1b | Full inventory + required-check guidance | `docs/WORKFLOWS.md` |
| G2a | Source `download-artifact` SHA pin | Source durable-source-bridge |
| G2b | `requirements.lock` + SECURITY contract | Source |
| G2c | CI installs use lock; remaining artifact pins | Source workflows |
| G3a | Identity freshness workflow (weekly) | Icon `identity-freshness.yml` |
| G3b | Drift → regenerate snapshot + open PR | Icon `identity-freshness.yml` |
| G4a | `PIPELINE_AND_PUBLISH` aligned with Architecture | Collection |
| G4b | Identity Boundary final (Clean V6) | Icon |
| G4c | Historical doc index | Icon `docs/HISTORICAL.md` |
| G5a | Durable Bridge selective matrix + policy file | Source |
| G6 | Cross-repo read model (generated-only) | `scripts/generate_ecosystem_release_status.py` + `ecosystem-status.yml` |
| G7 | Lifecycle × Freshness × Health × Lineage | `docs/STATE_MODEL.md` |
| G | Root `SECURITY.md` | Collection + Icon |

## Remaining

| ID | Item | Notes |
|----|------|--------|
| G4d | Move RISK/R14 into `docs/archive/` | Index exists; physical move optional |
| G8 | Published Raw E2E | Consumer-side verify after publish |
| G1c | Branch-protection required-check alignment | Repo settings (UI); docs already list recommended checks |

## Non-goals (explicit)

- No additional authoritative status databases
- No new gate workflows without retiring duplicates
- No handwritten coverage / service counts in README
