# Audit execution log 2026-10-08

Source report: strict cross-repo audit (governance + SSOT + size + durable + identity).

## Applicability

Verified against live main: SHAs, protection API, size_gate semantics, durable PARTIAL path, Icon snapshot drift — **claims match**.

## Executed

| ID | Action |
|----|--------|
| P0-1 | Branch protection: no force-push/delete on Collection/Source `main`, Icon `main`/`dist`/`state` |
| P0-2 | `size_gate.py` file vs tree semantics; transitional thresholds; **wired into `build.yml`** |
| P0-3 | Source Durable Bridge: COMPLETE-only may push main |
| P0-4 | Icon `collection_identity_snapshot.json` refreshed to Collection index SHA |
| P1 | Demote Collection `source_canary_state.yaml` SSOT role |
| P1 | Clarify `source_promotion_policy.yaml` vs live canary |
| P1 | Ecosystem lock schema + provenance doc |

## Deferred (needs artifact store / manual product decisions)

- Move `data/` / `backup/` off git (volume)
- Per-service Source authoring split
- Full ecosystem-release-lock generation in publish DAG
- `baidu` Collection identity accept
- Permissions split read-only vs publish jobs


## Wave 2 (continued)

| ID | Action |
|----|--------|
| Ecosystem Lock | `scripts/write_ecosystem_release_lock.py` + `publish.yml` step `--require-icon-identity` |
| Publish Size Gate | Size Gate before fail-closed policy gate |
| Durable PARTIAL | diagnostic branch `automation/durable-partial/<run_id>` + main only COMPLETE |
| company_targets | Source = SSOT_AUTHORITY; Collection = SSOT_MIRROR |
| Identity notify | `notify-icon-identity.yml` (needs `ICON_DISPATCH_TOKEN` for cross-repo) |
| Icon freeze doc | `docs/FREEZE_VS_IDENTITY.md` |

Still deferred: git volume offload (`data/`/`backup/`), required status checks + mandatory PR, full permissions split, baidu identity accept, auto lock client digests.
