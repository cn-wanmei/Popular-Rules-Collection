# Icon System Audit — 2026-09-30

## Audited repositories

- `cn-wanmei/Popular-Rules-Icon`
- `cn-wanmei/Popular-Rules-Collection`

## Canonical identity

Collection `rule/_index.yaml` contains **394 `entity: service` records**. Icon consumes that service universe through a pinned identity snapshot.

## Clean V6

- `icon-2026.09.30.clean1`
- 394/394 canonical services
- 0 production orphans
- 0 missing canonical IDs
- `ai` present
- 6304 variant records
- physical closure: 0 missing
- strict manifest gate: PASS
- release-writer build-and-gate: PASS
- release-writer publish: PASS

## Historical 89-orphan cleanup

The previous 482-record production state contained 89 non-canonical/historical identities. They were removed from the canonical production state. Their audit history is retained outside the production identity set.

## Identity boundary

Collection is the sole authority for `service_id`, `display_name`, and `provider`. Icon Registry is an asset consumer and cannot redefine service identity.

## V5

V5 fallback is now disabled. The remaining `assets/icons/v5` tree is a physical retirement target only and is not part of the runtime production path.

## Current status

- Phase A identity contract: complete.
- Phase B snapshot + gate: complete.
- Phase C registry normalization: complete for current production set.
- Phase D canonical clean release / object closure: complete.
- Phase E final V5 retirement: complete; runtime removed, fallback disabled, retirement gate conditions passed, and `assets/icons/v5` deleted.