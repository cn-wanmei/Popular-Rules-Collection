# Phase 7 — Legacy Finalization

## Goal
Turn the existing Legacy regression and reconciliation evidence into one terminal, auditable migration state.

## Contract
- Legacy regression must have zero unexplained removals.
- Legacy Asset Equivalence must be 100% and PASS.
- Legacy reconciliation must have zero structural drift and promotion remains blocked.
- Finalization is evidence-only and never writes V1 canonical assets.
- Finalization never authorizes deletion by itself.

## Production migration wiring

The Phase 8 final migration gate now generates the reconciliation evidence, aggregates regression + equivalence + reconciliation through `finalize_legacy()`, and treats the finalization report as a hard migration gate. The resulting `reports/v1/LEGACY_FINALIZATION_PHASE7.json` is carried into the release candidate and published evidence.

Finalization remains strictly non-destructive: it cannot switch SoT and cannot authorize Legacy deletion.

## Exit criteria
1. Regression, equivalence and reconciliation are represented by one report.
2. Missing evidence fails closed.
3. Promotion remains blocked until the explicit cutover sequence authorizes it.
4. Phase 8 cannot pass while finalization is incomplete.
