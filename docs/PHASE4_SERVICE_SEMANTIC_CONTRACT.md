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

## Production wiring

The V3 production DAG now executes `semantic_contract` immediately after IR generation and before directory validation and client adapters. A failing semantic report changes the production run to `blocked` and therefore cannot reach RC_READY publication.

The run persists a compact semantic contract at `data/runs/<run_id>/semantic/contract.json`, including the checked rule types so the final migration gate remains auditable even after the large `ir.json` is removed from the published repository tree.

## Exit criteria
1. Valid semantic IR passes.
2. Unknown references fail.
3. Invalid actions fail.
4. Conflicting per-entity decisions fail closed.
5. Production V3 runs cannot publish when the semantic contract fails.
