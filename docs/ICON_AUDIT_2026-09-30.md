# Icon System Audit — 2026-09-30

## Repositories audited

- cn-wanmei/Popular-Rules-Icon
- cn-wanmei/Popular-Rules-Collection

## Current canonical service universe

Collection main currently exposes 394 entries with entity=service in rule/_index.yaml.

## Current Icon V6 publication

Popular-Rules-Icon dist branch:
- release: icon-2026.09.30.r14
- manifest entries: 482
- canonical service IDs present: 393/394
- missing canonical ID: ai
- orphan dist/registry IDs: 89

Therefore the previous "100% Collection coverage" wording is not valid under the current identity-boundary definition; it counted non-canonical/orphan entries.

## Documentation/config drift found and corrected on this branch

1. Collection icon_v6.yaml pointed to styles8, while the actual dist manifest is r14.
2. Icon V6 cutover documentation referenced freeze1; actual dist is r14.
3. Collection V5 documents claimed Active/Production even though provider=v6.
4. Collection README advertised V4 as the active icon library.
5. V5 automation workflows could still mutate assets/icons/v5.
6. Icon R14/R20 documentation had conflicting status ("done" vs "in progress").
7. Icon release pointers claimed 100% Collection coverage despite 89 orphan entries and one missing canonical service.
8. Icon release manifest records .bin paths, while physical dist objects are .png; resolver currently constructs .png URLs.
9. Icon main `release.yml` is now a fail-closed V6 release writer; `incremental.yml` remains scaffold, so acquisition→state→release is not yet proven end-to-end.

## Production-chain verdict

V6 is present and serving a real dist branch, but the complete production chain is NOT yet proven healthy.

Blocking items before V5 removal:
- identity universe normalization;
- canonical 394/394 V6 coverage;
- zero production orphans;
- no V5 fallback dependency;
- manifest/physical-path consistency;
- reproducible release writer and end-to-end acquisition/release validation;
- resolver end-to-end verification against immutable manifest.

## Current project status

Collection:
- identity boundary contract: on migration branch;
- V6 default provider: active;
- V5: legacy fallback only;
- V5 automation: retired on this branch;
- V5 asset tree: retained pending retirement gate.

Icon:
- identity snapshot/gate: active migration tooling;
- R14 dist exists;
- identity normalization: in progress;
- R20 annual freeze: pending.

No current documentation should describe V5 as active production or describe R14 as 100% canonical Collection coverage.
