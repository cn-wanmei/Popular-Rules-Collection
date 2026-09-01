# Legacy 2.x Separation Plan

After Engine is sole production runtime:

## S0 Freeze (now)
`scripts/` production until cutover; Engine parallel under `src/engine/`.

## S1 Engine-only CI
`python -m src.engine.cli all`; scripts become thin shims.

## S2 Archive
`archive/legacy-2x/` + tag `legacy-2x-final`

## S3 Data boundary
`data/generated/` = workspace SSOT; `generated/` = public projection only.

## S4 Remove dual entry
Registry → `src.engine.*` only; naming gate fails on `src/v3`.

## S5 Rollback kit
Retain one full `generated/` release_id ≥1 cycle.
