# V3.0 Release Notes (2026-08-31)

## Completed
- **7 client builders** under `src/adapters/{mihomo,singbox,surge,shadowrocket,quantumultx,egern,loon}/build.py`
- **rule_loader** under `src/adapters/_common/rule_loader.py`
- **scripts/build_*.py** = compatibility shims (CI/entry stable)
- **builder_registry.yaml v2** with `module` field
- **Output paths unchanged** (`generated/*`)
- Hierarchy post-normalize + HARD (prior commit)
- `src/core` models/contracts (Phase 1)

## Intentionally deferred (plan alignment)
| Item | Why |
|------|-----|
| Canonical Rule Store (`database/canonical/rules*`) | Body still in `database/services` |
| Remove `legacy_body` | Migration mapping still required |
| Universal IR v2 entity/view fields | Additive later |
| Move all 100+ scripts into src/ | Only adapters moved |
| Delete legacy subscription paths | Forbidden |

## Verify
```bash
python scripts/pipeline.py preflight
python scripts/build_surge.py   # shim → src.adapters.surge.build
python scripts/hierarchy_golden.py
```
