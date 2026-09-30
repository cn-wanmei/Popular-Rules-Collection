# Icon V6 R5 Cutover

**Date:** 2026-09-30  
**Default provider:** `v6`  
**Release:** `icon-2026.09.30.freeze1`  
**Fallback:** V5 local assets if service missing in V6 manifest

## Rollback
Set in `config/icon_v6.yaml`:
```yaml
provider: v5
```

## Resolve
```bash
python scripts/icon_resolver_v6.py --service github
```
