# Phase 0 — Service Production Evidence & Governance (Locked)

**Status:** execution baseline (corrected plan)  
**Main anchor at seed:** post-PR #60 RC_READY runs under `data/runs/`  
**Does not rewrite V3 Engine core.**

## Five engineering invariants

1. **Release Evidence SSOT** is only  
   `data/runs/<run_id>/release/manifest.json` (`schema: release_manifest_v3`).
2. **Production Evidence is not a second Service SSOT.**  
   Config describes intent; run reports hold measured evidence; eligibility is derived.
3. **`release_eligible` / `production` are DERIVED** — never hand-written source fields.
4. **`database/services/*` is not V3 runtime input.**  
   Classify artifacts (`runtime_*` / `legacy_only` / `orphan` / …) before demanding Service Model materialization.
5. **`coverage = partial` ⇒ `production` forbidden** — CI-detectable invariant, not team discipline.

## KPI (current, factual)

| Metric | Value |
|--------|-------|
| P0 Identity Coverage | 50 / 50 |
| P0 Materialized | track via Service Model (Tencent A/B + Alibaba Batch 03 children) |
| P0 Materialized Full | 0 / 50 (all current materializations are `partial`) |
| Baseline file | `data/baseline/latest.json` (seeded Phase 0.1) |

Do **not** report Tencent Batch 02 as “Provider fully complete” — only Phase A/B completed; `qq` / `wecom` / `tencentmeeting` remain blocked.

## Layering

```
Config   → service_model / hierarchy / primary / intentional / service_production_policy.yaml
Run      → data/runs/<run_id>/release/manifest.json + reports/service_production_evidence.json
Derived  → release_eligible, production_evidence_complete, production
```

## Phase checklist

| ID | Item | Tooling |
|----|------|---------|
| 0.1 | Baseline reproducibility | `data/baseline/latest.json` seed from post-#60 RC_READY |
| 0.2 | Baseline contract | existing `baseline_evidence_v1` / `NO_BASELINE` neutral gate |
| 0.3 | Release manifest SSOT | locked path above |
| 0.4 | Post-promotion `latest_release` refresh | must follow Promotion SUCCESS (not bare Build) |
| 0.5 | Roadmap governance | this doc + policy |
| 0.6 | PR/branch hygiene | ongoing |
| 0.7 | Status consistency gate | `python scripts/status_consistency_gate.py` |

## Domain rule type hygiene (related hard gate)

Bare labels (`alibaba`, `google`, …) must **not** emit as `DOMAIN-SUFFIX` / `domain_suffix_set`.  
Normalized at ingest (`src/engine/ingest/normalizer.py`) and defended in adapters.

## Acceptance for Phase 0 exit

1. Diagnostic reproduction may use older runs (e.g. `20260917T052223793025Z-run`).
2. **Final acceptance requires a post-PR #60 RC_READY + Promotion run** on current `main`.
3. Status consistency gate PASS (warnings allowed for legacy `latest_release` until 0.4 lands in CI).
