# Phase 7 — Legacy Finalization

## Goal
Turn the existing Legacy regression and reconciliation evidence into one terminal, auditable migration state.

## Contract
- Legacy regression must have zero unexplained removals.
- Legacy Asset Equivalence must be 100% and PASS.
- Legacy reconciliation must have zero structural drift and promotion remains blocked.
- Finalization is evidence-only and never writes V1 canonical assets.
- Finalization never authorizes deletion by itself.

## Parallelization boundary
Phase 7 consumes evidence files already produced by the migration toolchain.
It can be implemented independently from Phase 6 observation and Phase 8 deletion.

## Exit criteria
1. Regression, equivalence and reconciliation are represented by one report.
2. Missing evidence fails closed.
3. Promotion remains blocked until the explicit cutover sequence authorizes it.
