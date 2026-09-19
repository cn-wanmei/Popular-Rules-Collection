# Phase 5 — Unified Release Engine

## Goal
Provide one production-facing release entrypoint that composes the existing V3
pipeline, RC_READY release gate, and atomic promotion implementation.

## Contract
- The engine runs the existing V3 pipeline.
- Promotion is attempted only when the run is RC_READY.
- Existing release and promotion gates remain authoritative.
- A blocked pipeline or non-RC_READY release cannot publish.
- The engine exposes one deterministic result schema for callers.

## Parallelization boundary
This PR composes existing components and can be developed independently from
the Phase 2, Phase 3, and Phase 4 focused contracts.

## Exit criteria
1. One release entrypoint exists.
2. Publish cannot bypass RC_READY.
3. Existing promotion validation remains unchanged.
4. CLI publish delegates to the unified engine.
