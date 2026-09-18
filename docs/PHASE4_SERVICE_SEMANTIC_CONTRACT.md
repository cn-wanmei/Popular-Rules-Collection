# Phase 4 — Service Semantic Contract

## Goal
Publish one fail-closed semantic contract at the service-facing IR boundary.

## Contract
- Entity references must resolve inside the IR entity universe.
- Memberships may reference only known rule IDs.
- Decisions must use DIRECT, PROXY, or REJECT.
- Decision type/value must match the referenced rule.
- A rule/entity pair cannot carry conflicting decisions.
- The validator adds behavioral checks without replacing the existing IR schema.

## Parallelization boundary
This PR consumes the existing IR shape only. It can be implemented and CI-tested
independently from the Phase 2 model facade and Phase 3 runtime gate.

## Exit criteria
1. Valid semantic IR passes.
2. Unknown references fail.
3. Invalid actions fail.
4. Conflicting per-entity decisions fail closed.
