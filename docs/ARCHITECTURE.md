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
    Canonical → Semantic IR
      ├─→ rule/                  human browse / search / selection
      └─→ generated/             client + network distributions
      ↓
    deterministic Release Candidate
      ↓
    atomic Git publish

## Truth layers

| Layer | Authoritative role |
|---|---|
| `sources/` | upstream source definitions |
| `backup/<date>` | immutable Collection input for a run |
| `data/runs/<run>/canonical` | V3 Canonical truth for that run |
| `data/runs/<run>/ir` | semantic intermediate representation |
| `rule/` | human-readable browse/search/selection release tree |
| `generated/<client>` | compiled client distribution |
| `generated/<network-scope>` | compiled companion datasets |
| `docs/` | architecture, usage and audit documentation |
| `rules/` | deleted; no alternate rule database |

`rule/` is generated from the same IR as `generated/`. It is not copied from one client, and neither `rule/` nor `generated/` is a source for the other.

## Atomicity

A Release Candidate contains both output projections and the same `run_id` / IR digest. Publish commits both directory trees in one Git commit. Rollback is Run-based and restores both together.

## Directory invariants

- Exactly one human rule tree exists: `rule/`.
- `rules/` must not exist.
- `rule/` contains generic, client-neutral rule records only.
- `generated/<client>/` is client-specific and never feeds `rule/`.