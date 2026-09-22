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
       └─ 7 client adapters
       ↓
    Determinism / Semantic / Directory / Evidence gates
       ↓
    Network Dataset Materialization
       ↓
    Release Candidate
       ↓
    Immutable Publish
       ↓
    generated/

Popular-Rules-Source is the upstream evidence supply layer. Collection owns Canonical, IR, client projection, release and final publication.

## What is final

The consumer-facing distribution is `generated/`.

Service rules are under:

    generated/mihomo/
    generated/singbox/
    generated/surge/
    generated/shadowrocket/
    generated/quantumultx/
    generated/egern/
    generated/loon/

Network companion datasets are under:

    generated/network/
    generated/geosite/
    generated/geoip/
    generated/provider/
    generated/asn/
    generated/ip/
    generated/policies/
    generated/mmdb/

`generated/manifest.json` inventories both groups. A publish is incomplete when a required Network Dataset scope is absent.

## Legacy trees

`rule/` is retained for V1 migration and human browsing. It is not a V3 runtime input.

`rules/` is the V3 directory-contract target. It is not an alternative database that must mirror `rule/` or `generated/`.

A difference between `rule/` and `generated/` is therefore expected and is not itself a production defect.

## Fail-closed rule

Generated artifacts are never edited manually to repair a missing route. Repair the upstream source or Canonical input, then rerun the V3 build and promote a new immutable release.