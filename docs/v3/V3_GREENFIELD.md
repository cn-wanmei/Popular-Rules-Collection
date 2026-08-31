# V3 Greenfield (not migration)

## Decision
Stop V2.7 → V3 file-by-file moves. V2 is **frozen baseline / oracle**.
V3 is a **new runtime** built in parallel under `src/v3/`.

## Layout
```
src/v3/          # independent runtime
config/v3/       # V3-only SSOT configs
data/v3/         # snapshots, canonical, artifacts (parallel)
tests/v3/        # golden / differential
docs/v3/         # contracts
reports/baseline/V2_FREEZE.json
```

## Phases
0 Freeze V2 (this commit)
1 Core Model + Schema contracts
2 Canonical + Ingest + Normalize engines
3 Entity Graph + Hierarchy + Decision
4 Universal IR v2
5 Seven Adapters → `data/v3/artifacts/`
6 Full Differential vs V2 oracle
7 RC + Cutover Manifest
8 V2 read-only legacy

## Do not
- Half-migrate `scripts/foo.py` → `src/foo.py` while production still uses scripts
- Teach V3 to call `legacy_body`
- Delete V2 subscription paths on day one
