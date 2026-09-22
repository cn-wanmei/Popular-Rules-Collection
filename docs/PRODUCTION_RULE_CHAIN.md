# Production Rule Chain

## Canonical chain

    Upstream sources
       ↓
    Collection DAG
       ↓
    backup/<date>
       ↓
    Immutable Source Lineage Gate
       ↓
    V3 Engine
       ├─ ingest
       ├─ source gate
       ├─ quarantine
       ├─ canonical
       ├─ hierarchy
       ├─ semantic IR
       ├─ human rule distribution → rule/
       └─ 7 client adapters → generated/<client>/
       ↓
    Determinism / Semantic / Directory / Evidence gates
       ↓
    Network Dataset Materialization → generated/<network-scope>/
       ↓
    Release Candidate
       ↓
    Immutable Publish
       ↓
    rule/ + generated/

## What is final

`rule/` is the user-facing browse/search/selection distribution. `generated/` is the client and network subscription distribution. Both are projections of the same immutable Run.

## Directory policy

`rule/` and `generated/` are sibling release projections. `rules/` is deleted and must not be recreated.

## Fail-closed rule

Generated and human-facing release artifacts are never edited manually to repair a missing rule. Repair the upstream or Canonical input, rerun the V3 build, and publish a new immutable Run.