# V1 Architecture Decision Record

## ADR-0001: Git is not runtime storage

Accepted. Git stores source code, configuration, schemas, tests, decisions and documentation only. Snapshots, CAS, runs, reports and generated releases belong to external artifact storage.

## ADR-0002: Offline build

Accepted. Builder consumes an immutable snapshot manifest and never accesses the network.

## ADR-0003: Explicit semantic loss

Accepted. Adapter output is classified as exact/equivalent/approximate/lossy/unsupported. Unsupported semantics are reported and may block release according to policy; they are never silently fabricated.

## ADR-0004: Last Known Good

Accepted. A failed or anomalous upstream snapshot cannot overwrite the last known good production input.

## ADR-0005: Phase 0 before migration

Accepted. Existing production data and legacy paths remain untouched until schemas, invariants and migration tests exist.
