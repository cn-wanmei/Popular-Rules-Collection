# Tencent Cloud Production Activation

**Date:** 2026-10-01  
**Service:** `tencentcloud`  
**Status:** production (legacy unlock)

## Binding

| Field | Value |
|---|---|
| snapshot_id | `snap-tencentcloud-e55bc8c508e839813ae20cd0` |
| content_digest | `073c3031c90820457209336550d39bbd4976b9f91c1486be5b0795a2c302057f` |
| source_release | `releases/tencentcloud/snap-tencentcloud-e55bc8c508e839813ae20cd0/release.json` |

## Qualification

- reconciliation_pass: true
- seven_client_semantic_pass: true
- rollback_pass: true
- observation_pass: true
- source_official_evidence_only: true
- production_unlock_run_id: operator-2026-10-01

## Note

Operator-promoted production binding on 2026-10-01. Archived for fail-closed
`source_production_gate` lineage. Do not treat this file as a runtime SSOT;
runtime identity remains `sources/immutable_registry.yaml` + Source durable seal.
