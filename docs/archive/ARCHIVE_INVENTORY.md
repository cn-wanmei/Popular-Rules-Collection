# Process artifact archive inventory (P1)

Generated 2026-10-07 as part of P0–P2 audit remediation.

## Rule

- **Do not delete** any path still referenced by `.github/workflows/*` or active `scripts/` without updating callers in the same PR.
- Prefer move to `docs/archive/phases/config/` only after `rg` + CI green.

## CI-held (must keep on config/ or scripts/ for now)

| Path / script | Referenced by |
|---------------|---------------|
| `scripts/phase_j_p0_service_evidence.py` | `build.yml` |
| `scripts/p0_batch01_semantic_overlap_audit.py` | `publish.yml` |
| Related `config/p0_batch01_*` | likely same scripts |

## Archive candidates (no workflow hit in spot-check; still verify before move)

### Config (process / batch)

- `canonical_root_migration.yaml`
- `phase_i_gate_closure.yaml` … `phase_o_r_operational_closure.yaml`
- `v1_final_migration_gate.yaml`
- `p0_batch02_*` … `p0_batch04_*` (except any still imported by active scripts)
- `p0_geosite_*`, `p0_source_bridge_*`, `p0_materialization.yaml`, bridges
- Snapshot dirs: `p0_batch01_snapshots/`, `p0_batch04_snapshots/`, `p0_geosite_snapshots/`, `p0_source_snapshots/`

### Scripts

List with `ls scripts | rg 'phase_|p0_|legacy_'` before moving. Keep `legacy_*.py` until `docs/LEGACY_STATUS.md` PASS.

## Recommended sequence

1. `rg 'p0_batch|phase_[j-o]|p0_geosite' -g '*.yml' -g '*.py'` on main
2. Move unreferenced yaml → `docs/archive/phases/config/`
3. Move snapshot trees → `docs/archive/phases/snapshots/` (or git-rm if pure historical blobs)
4. CI: build + publish dry paths still pass
5. Update this file with completion date

## Status

- 2026-10-07: inventory only; **no mass move** in this remediation branch (fail-safe).
