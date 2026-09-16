# Legacy migration boundary — archived

STATUS: ARCHIVED
OWNER: V3 Engine
PRODUCTION_USE: NONE
MIGRATION_DATE: 2026-09-16
DELETE_AFTER: 2026-09-16

The V2 migration compatibility layer has been audited and is no longer required by
production, CI, documentation, or tests. V3 production execution uses `src.engine`
exclusively.

Dependency scan performed before deletion covered `legacy/`, `scripts/`, `src/`,
`tests/`, `.github/`, `docs/`, and repository search for the retired parser and
normalizer paths. No production references were found. The tree is therefore
eligible for permanent removal; Git history remains the archival record.
