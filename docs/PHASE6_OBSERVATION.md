# Phase 6 — Observation

## Goal
Expose one read-only observation contract for a completed V3 run.

## Contract
- Metrics, parser coverage, source health, baseline evidence, quality and release state are summarized in one report.
- Observation never promotes or mutates a release.
- Missing or ERROR baseline evidence is a hard observation blocker.
- Only RC_READY or PRODUCTION runs are considered publishable observations.

## Parallelization boundary
Phase 6 consumes immutable run evidence already produced by the V3 engine.
It does not require the Phase 7 or Phase 8 branch and can be merged independently.

## Exit criteria
1. A deterministic observation report is emitted per run.
2. Evidence omissions fail closed.
3. Observation remains read-only.
