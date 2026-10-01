# Phase 1 — Artifact Classification & Production Invariants

## Goals

1. Classify historical service artifacts **without** promoting them into V3 runtime SSOT.
2. Enforce **`coverage=partial` ⇒ `production` forbidden** as a CI hard invariant.
3. Keep `release_eligible` / `production` **derived** from run evidence + policy only.

## Artifacts

| Path | Role |
|------|------|
| `scripts/classify_service_artifacts.py` | Classify legacy trees → `reports/artifact_classification.json` |
| `scripts/partial_production_invariant_gate.py` | Hard gate: partial never production |
| `scripts/derive_service_production_evidence.py` | Run-level derived eligibility (already Phase 0) |
| `config/service_production_policy.yaml` | Policy only (not evidence) |
| `config/evidence_policy.yaml` | Release / baseline / classification classes |

## CI wiring

- **Unit Tests**: `partial_production_invariant_gate.py` is **blocking**.
- **Unit Tests**: classification runs as **report** (writes `reports/artifact_classification.json` when legacy tree present).
- **Publish**: derive → refresh latest_release → status gate → evidence gate → invariant gate.

## Non-goals

- No `p0_service_production.yaml` parallel matrix.
- No forcing `legacy_only` / `orphan` into Service Model materialization.
- No marking partial services production by hand.

## Exit criteria (Phase 1)

- [x] Classifier exists and never writes service production SSOT
- [x] partial→production invariant is CI-detectable and blocking
- [ ] Classification report refreshed on main after full-tree checkout jobs
- [ ] Only `runtime_candidate` / model-backed services enter evidence completion work
