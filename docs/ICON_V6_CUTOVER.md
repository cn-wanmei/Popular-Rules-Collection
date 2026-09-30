# Icon V6 R5 Cutover — Final

**Date:** 2026-09-30  
**Default provider:** v6  
**Active dist release:** icon-2026.09.30.clean1  
**Manifest:** manifests/icon-2026.09.30.clean1.json  
**Canonical Collection service universe:** 394

## Verified production state

- Canonical services: 394/394
- Production orphan entries: 0
- Variant matrix: 8 styles × 128/256 = 16 per service
- Variant records: 6304
- Physical object closure: PASS
- Strict V6 manifest gate: PASS
- First clean release-writer build-and-gate: PASS
- First clean release-writer publish: PASS
- AI canonical service: present in clean release
- Independent V6 rollback: icon-2026.09.30.r14.1

## V5 state

V5 is no longer a production dependency. The Collection resolver uses V6 only and fallback_to_v5 is disabled.

The V5 asset tree remains temporarily on disk only until the explicit V5 retirement gate is run and the deletion PR is merged.

## Retirement sequence

1. verify clean1 production and rollback;
2. run V5 retirement gate;
3. delete assets/icons/v5;
4. remove remaining V5-only documentation/config references;
5. rerun Collection validation and publish gates.
