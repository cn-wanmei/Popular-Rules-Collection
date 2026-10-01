# Phase 6 — Observation

## Goal
Expose one read-only observation contract for a completed V3 run.

## Contract
- Metrics, parser coverage, source health, baseline evidence, quality and release state are summarized in one report.
- Observation never promotes or mutates a release.
- Missing or ERROR baseline evidence is a hard observation blocker.
- Only RC_READY or PRODUCTION runs are considered publishable observations.

## Production wiring

Observation is the terminal read-only stage of the V3 production DAG, immediately after release evaluation. Every full production run must emit `data/runs/<run_id>/observation/report.json`; a blocked observation changes the overall run status to `blocked` and prevents publication.

## Exit criteria
1. A deterministic observation report is emitted per run.
2. Evidence omissions fail closed.
3. Observation remains read-only.
4. Publication requires a passing observation report.
