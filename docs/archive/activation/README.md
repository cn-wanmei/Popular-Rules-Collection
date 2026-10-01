# Activation & Freeze Archive

Historical production freeze and activation records. These files are **immutable evidence**, not current operational policy.

| Record | Date | Meaning |
|---|---|---|
| [MAIN_FREEZE_2026-09-20.md](MAIN_FREEZE_2026-09-20.md) | 2026-09-20 | Soft freeze of automated writers during Phase 2 Source re-audit |
| [UNFREEZE_ACTIVATION_2026-09-22.md](UNFREEZE_ACTIVATION_2026-09-22.md) | 2026-09-22 | Controlled unfreeze; writers resume under gates only |
| [TAOBAO_PRODUCTION_ACTIVATION_2026-09-22.md](TAOBAO_PRODUCTION_ACTIVATION_2026-09-22.md) | 2026-09-22 | Formal taobao production activation evidence |

## Current policy

- Production is **not** frozen (as of Unfreeze 2026-09-22).
- Direct arbitrary `main` mutation remains prohibited.
- Collect / Publish / Status writers run under fail-closed gates.
- Live publish metrics: root [`PUBLISH_STATUS.md`](../../PUBLISH_STATUS.md) (CI-generated).
- Hard branch protection / rulesets: see Issue #122 (must be confirmed in GitHub Settings).
