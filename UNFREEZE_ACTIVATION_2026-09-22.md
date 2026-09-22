# Unfreeze / Activation Record — 2026-09-22

schema: unfreeze_activation_v1
activation_date: 2026-09-22
freeze_reference: MAIN_FREEZE_2026-09-20.md
status: released
activation_mode: controlled

scope:
  collect_writer: controlled
  status_writer: controlled
  publish_writer: gated
  icon_writer: branch_pr_only
  retention_apply: gated

controls:
  direct_main_mutation: false
  required_pr_or_protected_automation: true
  required_ci_gates: true
  fail_open_allowed: false

activation_conditions:
  main_freeze_lifted: true
  policy_state_parity_required: true
  immutable_lineage_required: true
  publish_gate_fail_closed_required: true
  production_lifecycle_requires_activation_evidence: true

current_transition:
  taobao:
    state: production
    collection_promotion: formally_activated
    activation_record: TAOBAO_PRODUCTION_ACTIVATION_2026-09-22.md
    production_unlock_run_id: '35680687328'
    note: "Formal production activation is backed by the existing machine-verifiable Canary evidence bundle."
  tmall:
    state: verified
    enabled: false
    lineage_action: align_to_immutable_registry_and_reverify
  publish:
    fail_open_issue: remediated_in_this_change_set
    all_known_ignored_failures_removed: true

guardrails:
  - "Unfreeze does not permit arbitrary direct main mutation."
  - "Automated writers remain controlled by PR / release gates."
  - "A missing, stale, failed, or unknown gate blocks production promotion."
  - "Historical freeze evidence remains immutable."
  - "Every lifecycle transition must retain source, snapshot, digest, run and activation provenance."

recorded_at: 2026-09-22
