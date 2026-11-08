# Production baseline pointer reconciliation — 2026-11-08

## Finding

`baseline/latest.json` referenced a non-existent run:

- Run: `20260918T175019058992Z-run`
- Snapshot: `snap-20260918T175019059736Z`

The run directory and its run manifest have no Git history in this repository. The pointer was therefore dangling and could not be used as auditable retention provenance.

## Verified replacement

The existing `data/baseline/latest.json` points to:

- Run: `20260917T054015320743Z-run`
- Snapshot: `snap-20260917T054015321635Z`

The referenced run is tracked in `data/runs/`, its run manifest reports `status=ok` and `release.state=RC_READY`, its quality report is `PASS` with all hard checks passing, and its collection manifest is tracked at `backup/2026-09-17/manifests/_collection.json`.

The records in the dangling production pointer and the tracked baseline pointer are identical: 259,570 clean/ingested/memberships, 128,714 unique rules, zero ingest/canonical errors, and zero quarantined records.

## Action

The production baseline pointer now references the tracked, verified run and snapshot above. No rule data, generated clients, backup artifacts, Source bindings, or Icon assets were changed.

This restores an auditable baseline → run → snapshot → collection-manifest chain and allows retention to protect the complete referenced chain.
