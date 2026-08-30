# Brand color fill + identity fixes

## Rules

1. Mono SI SVG → inject `brand.color` on paths (no AI redraw)
2. Official black only: apple/github/x/notion/…
3. Huawei ← Simple Icons path + `#CF0A2C`
4. `china` ← national flag (region icons)

```bash
python scripts/icon_color_identity_fix.py
python scripts/build_icons.py --force
python scripts/icon_engine.py --force
python scripts/icon_contact_sheet.py
```
