# Release 1.0.0

**Architecture:** V3 greenfield (`src/v3/`)  
**Production path:** still V2 (`scripts/` + Collect) until `production_cutover=true`

## Included
- Canonical Rule Store
- Hierarchy View Resolver + Decision
- Universal IR v2 (focus + full streaming)
- Snapshot + Quarantine
- 7-client adapters
- Golden L1–L7
- Differential vs V2 oracle
- Cutover Manifest

## CLI
```bash
python -m src.v3.cli all
```

## Policy
`CUTOVER_MANIFEST.production_cutover` remains false until human approval.
Rollback = last V2 `generated/` artifacts.
