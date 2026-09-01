# Architecture (1.0)

- **Product version:** 1.0.x (`VERSION`)
- **Engine codename:** v3 (metadata only; **not** a directory name)
- **Runtime package:** `src/engine/`
- **Workspace:** `data/generated/`
- **Public tree:** `generated/` (projection only; not SSOT)
- **Legacy:** `scripts/` until cutover — see `docs/LEGACY_2X_SEPARATION.md`

```
sources → engine pipeline → data/generated → (gates) → publish → generated/
```
