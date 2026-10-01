# Taobao Production Activation — 2026-09-22

schema: source_production_activation_v1
service_id: taobao
status: activated
activated_at: 2026-09-22

source:
  repository: cn-wanmei/Popular-Rules-Source
  source_commit: ffc7375b31080ea735c8bcc8ee59066b969c382f
  verified_input_commit: 4cfabcfc3e77806bc054035162ae64f93fa0505b
  snapshot_id: snap-taobao-d34b149646aa56450032d01d
  content_digest: cfd55feeff484e929a6ae7d440b00b424ac10d3c68e0ad77aa09d164e9db9719

collection_canary:
  workflow_run_id: 35680687328
  workflow_run: Phase 2 Source Canary
  artifact_id: 10674478298
  artifact_digest: sha256:e321105cc24945769d855b48a8eea6e64d1ca898ac2cbb22f1750256f682fec2
  canary_status: PASSED
  golden_pass: true
  seven_client_semantic_pass: true
  reconciliation_pass: true
  rollback_pass: true
  observation_window_started: true
  production_ready: true

evidence:
  reconciliation_run_id: reconcile-taobao-eae5cfc5d54bc726
  v3_run_id: canary-taobao-release-2
  semantic_run_id: canary-taobao-release-2
  rollback_run_id: rollback-taobao-6a64e023e0eddcdb
  observation_run_id: observe-taobao-ed5b9063e584f5c4
  observation_started_at: 2026-09-22T02:48:27.399246+00:00
  production_unlock_run_id: '35680687328'
  production_unlock_evidence: taobao-canary/production-unlock.json

activation_policy:
  direct_main_push: false
  activation_record_required: true
  immutable_lineage_required: true
  source_official_evidence_only: true
  seed_only_count: 0
  conflict_count: 0

result:
  previous_state: canary
  new_state: production
  enabled: true
  rollback_target: canary-taobao-release-1
  production_promotion_reason: "All machine-verifiable Production Unlock prerequisites in the existing Canary evidence bundle passed."

notes:
  - "The Source release remains provenance-bound to the immutable registry."
  - "The activation is recorded separately from the Source Canary implementation PR."
  - "No unverified run ID or synthetic evidence has been introduced."
