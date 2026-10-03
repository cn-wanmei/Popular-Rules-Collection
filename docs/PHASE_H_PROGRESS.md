# Phase H — Verification & Recovery Hardening

> **Status: Current tracker** (not SSOT)

## Completed

| ID | Item |
|----|------|
| H1 | Raw E2E HTTP fail-closed |
| H2 | Raw E2E 7 clients + leaf samples |
| H3 | Icon exact SHA + file_sha + full identity compare |
| H4 | Freshness remediation hard-fail |
| H4-fix | identity-freshness.yml YAML repair (multiline PR body broke parse → 0-job failure) |
| H5 | Event-driven ecosystem read model |
| H6 | Read Model readability + semantic_consistency |
| H7 | Durable `batch_completeness` |
| H8 | Source CI_AUTOMATION cleanup |
| H9 | `recovery-drill.yml` read-only probes |
| H10 | `docs/DISASTER_RECOVERY.md` |

## Notes

- First successful Identity Freshness after H3 may open a **snapshot sync PR** (pinned ref/file_sha lag behind Collection HEAD) — expected; review and merge.
- Branch protection UI remains optional (operator choice).

## Non-goals

- No fourth SSOT
- No architecture rewrite
