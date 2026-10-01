# Icon V6 Shadow Switch (R4)

Config: `config/icon_v6.yaml`

## How to operate

1. **Production (default):** `provider: v5` — unchanged behaviour.
2. **Shadow test:** set `provider: v6` on a branch / local build.
3. Resolver should:
   - load Icon physical manifest `manifests/icon-2026.09.29.1.json` from `Popular-Rules-Icon@dist`
   - map `service_id` → `variant_hash` → URL via mirrors
   - if missing and `fallback_to_v5: true`, use V5 path
4. **Rollback:** set `provider: v5` (or use `rollback.provider`).

## Canary (R1–R3)

Ten Tier-0 services published on Icon `dist` branch as release `icon-2026.09.29.1`.

## R5 cutover (not yet)

Only after shadow diff report is accepted; then change default `provider` to `v6`.
