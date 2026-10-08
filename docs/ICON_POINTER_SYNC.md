# Icon production pointer sync (Collection ↔ Icon)

## SSOT

| Field | Authority |
|-------|-----------|
| production / rollback release_id | **Icon** `config/release-pointers.yaml` |
| Collection consumer pins | `config/icon_v6.yaml`, `config/icon_docs.yaml` |

## Gate

```bash
python scripts/check_icon_pointers.py
```

Already required in `.github/workflows/validate.yml` (Icon docs V6 consumer gate).

## After Icon promote

1. Read Icon `production` and `rollback` from `release-pointers.yaml`.
2. Update Collection:
   - `icon_v6.yaml` → `v6.release_id`, `v6.manifest_path`, `rollback.release_id`, `rollback.manifest_path`
   - `icon_docs.yaml` → `production_release_id`
3. Run `check_icon_pointers.py` until OK.
4. Commit on Collection main (or PR).

Do **not** invent release IDs on Collection; always copy from Icon.
