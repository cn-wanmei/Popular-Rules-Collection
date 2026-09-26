# Icon System V5.1 — Source Quality

Principle: **Source First → Quality Gating → Seed Fallback → Render → Limited Post-process**

## Quality tiers (`source_px = max(w,h)`)

| Tier | Condition |
|------|-----------|
| high | SVG / vector, or `source_px >= 256` |
| medium | `128 <= source_px < 256` |
| acceptable | `96 <= source_px < 128` |
| low_res | `source_px < 96` |

## Acquisition order

1. Official SVG / brand CDN  
2. Apple Touch Icon  
3. High-res PNG (≥128, prefer ≥256)  
4. ICO **largest frame**  
5. favicon (last network resort)  
6. Reviewed seed (`assets/icons/seed/`) if better quality  
7. Semantic glyph  

`<96px` candidates are **rejected** by default unless no better source exists.

## Registry fields

`source_px`, `quality`, `source_type`, `official`, `fallback`, `seed`, `frame_count`, `selected_frame`

## CI

`icon_system_v5.py gate` warns on low_res; **FAIL** if listed in `quality.core_services_fail_low_res`.
