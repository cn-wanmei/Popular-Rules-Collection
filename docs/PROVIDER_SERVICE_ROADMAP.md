# Provider → Aggregate → Service Roadmap

This roadmap formalizes the ruleset hierarchy and the 180-service gap inventory approved for the current expansion phase.

## 1. Formal hierarchy model

A multi-service provider has one explicit aggregate ruleset and zero or more sibling service rulesets:

```text
Provider
├── Aggregate: provider
├── Service: service_a
├── Service: service_b
└── Service: service_c
```

The aggregate represents provider-wide coverage. A service is independently subscribable and independently testable. An aggregate may contain provider-direct memberships plus the union of declared child services.

Hierarchy metadata lives in `config/ruleset_hierarchy.yaml`. Production rule materialization remains governed by collected source membership, semantic probes, and the seven-client gate.

## 2. Adjustment principle

Never infer provider identity from a service name prefix. A string such as `google-calendar` must not automatically create provider `google`.

Provider, aggregate, parent service, aliases, and service status are explicit data. Unknown legacy entities remain `unmodeled` until declared.

Existing registry identities are not silently renamed. Split migrations use `status: split`, preserving current aggregate compatibility while introducing an independent service node.

## 3–11. Candidate gap domains

The candidate catalog covers domestic provider decomposition, domestic high-frequency independent services, international AI, Developer/Cloud/SaaS, Social/Communication, Media/Video/Music, Shopping/Travel/Payments, Gaming, and Search/Mail/Productivity.

The full inventory is in `config/service_candidates.yaml` and includes 180 planned/existing/split nodes.

## 12. Consolidated inventory

Target pool:

- 180 service nodes
- P0 target: 50
- P1 target: 70
- P2 target: 60

These are a planning pool, not a claim that all 180 currently have verified registry sources.

## 13. P0 — first 50

`config/p0_materialization.yaml` is the execution queue. Each node must pass:

1. exact upstream path verification;
2. collection into an immutable snapshot;
3. canonical membership creation;
4. semantic probes, including false-positive probes where keyword semantics are involved;
5. cross-client projection and seven-client gate;
6. only then registry activation/publication.

The first 50 intentionally combine provider decomposition (Apple/Tencent/Alibaba/ByteDance/Baidu/NetEase) with high-value AI, developer, social, media, commerce, travel, payment, and gaming services.

## 14. P1 — second batch

P1 expands the provider trees and adds stable SaaS, enterprise, international media, payment, travel, and regional services after P0 establishes the ingestion/materialization pattern.

## 15. P2 — third batch

P2 is long-tail but independently useful services. They should be activated only where source freshness, rule density, and semantic distinctness justify a standalone artifact.

## 16. Architecture change

The pipeline should now be understood as:

```text
Upstream sources
  ↓
Collection / immutable snapshot
  ↓
Ingest / Canonical
  ↓
Explicit Provider Identity
  ↓
Aggregate + Service hierarchy
  ↓
Semantic Intent
  ↓
Decision / IR
  ↓
Client Projection × 7
  ↓
Semantic Probe + Cross-client Gate
  ↓
Publish
```

The legacy hierarchy resolver has been changed from prefix-based inference to this explicit model. Backward-compatible `groups.jsonl` output is retained but no longer populated through name heuristics.

## Source strategy

Priority should be given to already configured high-trust upstreams: BlackMatrix7, MetaCubeX meta-rules-dat, v2fly domain-list-community, and Dler where appropriate. The current registry already contains many provider-level entries and several Apple sub-service source files; the new layer makes those relationships explicit rather than relying on a shared `name: apple` identity.

## Safety against false completeness

A candidate appearing in the catalog does not mean the rule has been collected, verified, or published. `source_status: verified_upstream`, `candidate_upstream`, and `new_source_needed` separate observed upstream coverage from future work.
