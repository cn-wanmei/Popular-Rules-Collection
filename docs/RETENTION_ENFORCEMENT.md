# Retention enforcement

SSOT: `config/retention.yaml`  
Planner: `scripts/retention.py` (default dry-run; `--apply` is destructive in the local checkout)

## Workflow

`.github/workflows/retention.yml` is intentionally non-destructive:

| Trigger | Behavior |
|---------|----------|
| Weekly schedule | Dry-run + upload `retention_plan.json` and `retention_plan.txt` |
| `workflow_dispatch` | Dry-run + upload plan |
| `pull_request` touching retention inputs/data | Dry-run + upload plan |

The workflow must not use `--apply`: deleting files inside an ephemeral Actions runner does not persist a repository cleanup commit and can falsely report success.

## Retention semantics

- `backup/`: retain successful snapshots for `keep_days` and at least `keep_min_successful`; current snapshots require a valid `collection_manifest_v1` whose date and root match the directory. Legacy registry-v3 snapshots are eligible only after every declared local file's path, size and SHA-256 have been verified against `manifests/_day.json`. Partial legacy backups use `backup.failed_keep_days` (14 days by default); malformed or unverifiable snapshots are protected.
- `data/runs/`: apply the run and failed-run windows only when no longer protected by references or embedded release evidence.
- `data/runs/<run>/release/`: `release/manifest.json`, `state.json`, and `sbom.json` form the embedded release-evidence set. Because this evidence is stored inside the run directory and no external artifact-store migration is complete, the whole run directory is retained for `release_evidence.keep_days` (180 days by default). A malformed or incomplete evidence set is protected as unknown.
- Provenance references are transitive: every retained run pins its snapshot and its `collection_manifest` backup; baseline/release pointers additionally pin the referenced run. A missing backup target or unresolved run-to-backup provenance blocks `--apply`.
- `reports/YYYY-MM-DD/`: apply the report window only after checking nested audit/release evidence and `source-health.md` history. Health history and release/audit evidence use their longer policy windows.
- Non-date report areas, archive, quarantine, audit, and current generated client distributions are preserved until their exact consumers and layouts are independently inventoried.
- `generated/_promotion/latest.json` and its referenced promotion record are protected; unreferenced timestamped promotion records remain for the release-evidence window and become candidates only after that window expires.
- Unknown names, malformed timestamps, missing manifests, and unresolved run/snapshot references are never delete candidates. Any dangling authoritative run or snapshot reference blocks `--apply`.

## Applying repository cleanup

1. Inspect the full JSON plan and resolve every blocking issue.
2. Review each candidate against the baseline, release pointer, SBOM, audit and health-history references.
3. Create an explicit deletion commit/PR in the repository; do not treat local `--apply` in a temporary runner as a persisted cleanup.
4. Run the full CI/build/release gates after the cleanup commit.

## Artifact-store dependency

The tracked tree still contains large `data/runs/` and `backup/` payloads. Until the Artifact Store migration has persisted and verified immutable external URIs/digests, retention must preserve the full run directories while embedded release evidence is inside them. See `docs/ARTIFACT_STORE_MIGRATION.md`.
