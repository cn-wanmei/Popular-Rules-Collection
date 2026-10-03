# Phase G — Governance & Convergence (progress)

> **Status: Current operational tracker**  
> Not a SSOT. Production numbers remain in `PUBLISH_STATUS.md` / Source lifecycle / Icon pointers.

Audit basis: 2026-10-03 cross-repo audit (Architecture ready → Governance focus).

## Completed

| ID | Item | Where |
|----|------|--------|
| G1a | Workflow classification index | `docs/WORKFLOWS.md` |
| G2a | Source `download-artifact` SHA pin | Source durable-source-bridge |
| G2b | `requirements.lock` + SECURITY contract | Source |
| G2c | CI installs use lock; remaining artifact pins | Source workflows |
| G3a | Identity freshness workflow (weekly) | Icon `identity-freshness.yml` |
| G4a | `PIPELINE_AND_PUBLISH` aligned with Architecture | Collection |
| G4b | Identity Boundary final (Clean V6) | Icon |
| G4c | Historical doc index | Icon `docs/HISTORICAL.md` |
| G | Root `SECURITY.md` | Collection + Icon |
| G5a | Durable Bridge selective matrix + policy file | Source `durable_release_policy.yaml` |

## In progress / next

| ID | Item | Notes |
|----|------|--------|
| G1b | Reduce `action_required` noise / required-check list | Label only; do not delete gates blindly |
| G3b | Auto-open Icon snapshot PR on drift | Freshness job currently fails on drift; PR automation optional |
| G4d | Move RISK/R14 into `docs/archive/` | Index exists; physical move optional |
| G6 | Cross-repo read model (generated-only) | No fourth SSOT |
| G7 | Lifecycle × Freshness × Health × Lineage fields | Contract doc |
| G8 | Published Raw E2E | After publish |

## Non-goals (explicit)

- No additional authoritative status databases
- No new gate workflows without retiring duplicates
- No handwritten coverage / service counts in README
