# Official icon packs

Place `{icon_id}.svg` here, then:

```bash
python scripts/icon_import_official.py --id wechat ./wechat.svg
# or copy manually to assets/icons/official/wechat.svg
python scripts/icon_p2_apply.py
python scripts/build_icons.py --force
```

Prefer brands listed in `metadata/official_whitelist.yaml`. Do not use favicon dumps as permanent assets.
