# Legacy (`database/`) deletion status

> **Status (2026-10-06 audit):** Legacy **NOT** authorized for deletion.

## Phase 8 Final Migration Gate (from `docs/RELEASE_AND_QC.md`)

Catalogue Coverage 100% alone is **not** sufficient.

Required before any automated or manual delete of `database/`:

| Requirement | Current assessment |
|-------------|--------------------|
| Catalogue Coverage 100% | Track via V3 run evidence |
| Legacy Asset Equivalence Coverage 100% (zero missing Legacy AssetKeys) | **Must re-verify** on latest immutable Snapshot |
| Phase 4 Golden all required dimensions | Evidence in `data/runs/` |
| Phase 5 all seven client artifacts + required rule kinds | V3 run |
| Phase 6 three complete V3 builds on same Snapshot | Check run history |
| Phase 7 zero unexplained removed assets | Audit report |
| Same V3 run `RC_READY` with `v2_runtime_dependency=0` | Gate JSON |
| Evidence bound to current commit | Mandatory |

- **Legacy Source:** `database/services/`
- **V1 Canonical:** `rule/`
- The final gate **never** deletes Legacy automatically (`scripts/legacy_delete.py` is gated).

## Operational rule

Until a dated PASS record is committed under `docs/archive/audits/` with the above checklist signed off:

1. Do **not** remove `database/`.
2. Do **not** remove `scripts/legacy_*.py`.
3. Prefer read-only reference; all production identity is `rule/_index.yaml` + IR.

## Next action

Run Phase 8 equivalence report on the latest production Snapshot and attach evidence path here when PASS.
