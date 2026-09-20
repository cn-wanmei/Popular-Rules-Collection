# Publish & CI status

Repository: cn-wanmei/Popular-Rules-Collection

**Production path:** V3 Engine → immutable run → 7 clients → release gate → atomic promotion.

<!-- AUTO-GENERATED:BEGIN -->
## Automated status

This section is maintained by CI.

### Production clients

- egern
- loon
- mihomo
- quantumultx
- shadowrocket
- singbox
- surge

### Release model

generated/ is the V3 publication projection.

### Legacy boundary

database/services/ remains retained until the explicit Phase 8 deletion gate becomes valid.

<!-- AUTO-GENERATED:END -->

## Human Notes

### Popular-Rules-Source

PRS is registered in the Collection Source Registry but is currently disabled.

Do not treat PRS candidate Source outputs as Production Coverage until its official-evidence-only Release and Collection Reconciliation both pass.

### Operational interpretation

Production status must be judged from the immutable run, release evidence, current commit and corresponding Gate. A single upstream or CI failure is not sufficient to invalidate the last successful release.
