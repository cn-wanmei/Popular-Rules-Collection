# Modern Brand Icon Grid v2

Contact sheet only (audit / docs). Client paths unchanged.

## Rules

- Canvas `#F7F7F8`, white cards, light border
- Optical crop via alpha bbox + max edge 44px
- Brand sheet vs Semantic sheet (no rainbow frames on brands)
- No AI brand redraw

```bash
python scripts/icon_contact_sheet.py
# → reports/icons/contact-sheet.png
# → reports/icons/contact-sheet-semantic.png
```
