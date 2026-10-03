# Tmall Production Activation

**Date:** 2026-10-01  
**Service:** `tmall`  
**Status:** production

## Binding

| Field | Value |
|---|---|
| snapshot_id | `snap-tmall-17de7049e2f7bf67cb88c785` |
| content_digest | `89e2ce020e9bb3a7538b80836127c59290470c896aa2a42438011eecce6dbc98` |
| source_release | `releases/tmall/snap-tmall-17de7049e2f7bf67cb88c785/release.json` |
| verified_input_commit | `76f18b76ca41f5ce551a035e1163d492a33db80a` |
| production_unlock_run_id | `36802753035` |

## Qualification

- reconciliation_pass: true
- seven_client_semantic_pass: true
- rollback_pass: true
- observation_pass: true
- source_official_evidence_only: true
- production_unlock_qualification: PASS

## Note

Canary run 36802753035 unlocked production on 2026-10-01. Archived for
fail-closed `source_production_gate`. Runtime identity remains immutable registry.
