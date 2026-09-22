# Architecture

## Single production DAG

    upstreams
      ↓
    collect
      ↓
    immutable backup/<date>
      ↓
    V3 Engine
      ↓
    Canonical → Semantic IR → 7 Client Adapters
      ↓
    deterministic Release Candidate
      ├─ generated/<client>/...
      └─ generated/<network-scope>/...
      ↓
    atomic publish

## Truth layers

| Layer | Authoritative role |
|---|---|
| `backup/<date>` | immutable Collection input for a run |
| `data/runs/<run>/canonical` | V3 Canonical truth for that run |
| `data/runs/<run>/ir` | semantic intermediate representation |
| `generated/<client>` | compiled client distribution |
| `generated/<network-scope>` | compiled companion datasets |
| `generated/manifest.json` | file-level publication inventory |
| `rule/` | legacy V1 browse/migration tree only |
| `rules/` | V3 directory contract target, not a second database |

## Source integration

Popular-Rules-Source is upstream Evidence Supply. Collection consumes its immutable release through exact commit SHA and provenance v2 equality. Source never writes Collection Canonical or client output.

## Network Dataset integration

Network Dataset refresh is separated from Service Identity semantics but is part of the same release DAG. Collection refreshes `database/` during Collect and the Build stage materializes the exact committed inputs into `release-candidate/generated/`.

Because Build performs no Network Dataset network fetch, the same Collection commit can be replayed deterministically.

## Directory invariants

- `generated/<client>/` is the only final Service Rule distribution namespace.
- `generated/<network-scope>/` is the only final Network Dataset distribution namespace.
- `rule/` and `rules/` are never used as a reason to hand-edit generated files.
- Provider, ASN, GeoIP and Geosite datasets cannot establish Service ownership by themselves.
- A Release Candidate without required Network Dataset scopes is incomplete.