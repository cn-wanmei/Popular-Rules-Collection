# Icon Identity Boundary V1

## Authority

Popular-Rules-Collection owns the canonical service identity.

Canonical published source:
- rule/_index.yaml
- entity == service
- service_id / display_name / provider

Popular-Rules-Icon consumes that identity and supplies icon assets. It is not a second service catalog.

## Prohibited drift

Icon Registry MUST NOT:
- rename a Collection service because an App Store result has a different name;
- replace a parent brand identity with a child-product identity;
- replace a child service identity with a parent brand identity;
- infer service equality from identical image bytes;
- treat a provider aggregate/category as an ordinary service.

## Canonical relationship

Collection service_id -> Icon Registry service_id -> icon asset

The same icon bytes may be intentionally shared by multiple service IDs. Sharing bytes does not merge identities.

## Synchronization

Icon Repository pins a Collection commit into a deterministic identity snapshot. Any Collection identity change requires a new snapshot and a new boundary-gate run.

## Migration

A. Contract: complete
B. Snapshot + gate: complete in Icon Repository
C. Registry normalization: in progress
D. Asset identity review: pending
E. Strict CI: pending until C/D are clean
