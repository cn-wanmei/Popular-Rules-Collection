# Popular-Rules-Source Integration

## Purpose

Popular-Rules-Source (PRS) is a Supplemental Source provider for missing or partial service coverage.

## Current state

The Collection Registry contains the PRS entry, but it is intentionally disabled.

~~~
popular-rules-source
enabled: false
~~~

The reason is strict: current PRS outputs are still Candidate/Review material in source space. Collection must not consume them as trusted production source until the Source Evidence Contract is satisfied.

## Expected Contract

PRS publishes a Source Release containing:

- service
- domains / assets
- evidence references
- provenance
- snapshot identity
- checksums
- reconciliation metadata

Collection consumes the release through the existing Source Registry / collection path.

## No direct cross-layer writes

PRS must never:

- modify Collection Canonical
- modify Collection IR
- write client output trees
- bypass Collection release gates

## Re-enable requirements

Before enabled=true:

1. Official source fetch is live and reproducible.
2. Seed-only assets = 0 for the promoted service.
3. Evidence linkage is complete.
4. Service boundary and exclusion checks pass.
5. Conflict count = 0.
6. Snapshot is deterministic and immutable.
7. Collection reconciliation passes.
8. A normal Collection V3 run consumes the Source successfully.

## Source services

First-wave targets:

1688, cainiao, dingding, qqmail, qqmusic, taobao, tencentcloud, tmall。

Tencent Cloud is treated as PARTIAL because an existing Collection Registry mapping already exists.
