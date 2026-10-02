# SERVICE_HIERARCHY V2.5 — Frozen Spec (Draft-3.1.1)

**Status:** Schema Freeze  
**Scope:** Spec + Schema + Validator + Resolver + Google Pilot (core/shared + ≤5 services).  
**Not:** bulk 60+ services, auto attribution, default Builder switch, V3 src/.

## Invariants

1. Provider = entity; Aggregate = View (not fetch target).
2. Hierarchy = DAG; V2.5 group depth ≤ 2.
3. Canonical Rule once; Service/Group/Aggregate are views.
4. Membership ≠ Ownership ≠ Dependency ≠ Infrastructure.
5. Shared infrastructure first-class; **explicit only**.
6. Coverage / Materialization / Lifecycle separated.
7. Aggregate = deterministic Union(explicit services + shared + **provider-core**). No YAML copy for sum.
8. Source only on Dataset/Canonical; views must not fetch.
9. Exclusive requires provable assignment; no auto-split from aggregate upstream.
10. Resolver deterministic + Resolver Manifest.

## Aggregate math (P0-16)

```text
Aggregate(provider) = Union(services, shared, provider_core)
```

## Resolve order

include → nested groups → exclude → materialization → normalize → dedup → sort → hash → emit+manifest

## Materialization priority

`service_model` > `intentional_unmaterialized` > legacy inference

## Forbidden

Bulk 60+ Google; auto attribution; aggregate source fetch; builder membership logic; default mihomo switch; delete categories/intentional; mass SID rename; V3 src/.

## Google pilot

`google-core` (loads legacy `database/services/google.yaml` body), `google-shared`, optional exclusive candidates (`gmail`, `google-search`), aggregate `google`.

## Golden

- L4: aggregate hash == union hash  
- L5: same snapshot Legacy(S) vs Aggregate(S)
