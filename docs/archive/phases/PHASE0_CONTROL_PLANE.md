# Phase 0 — Control Plane Closure

## Objective

Phase 0 does not expand the service catalogue or add new adapters. It closes the control-plane drift identified by the repository audit before the V1 runtime cutover begins.

## Scope

- Make Phase 8 coverage reporting mathematically exact.
- Keep operational baseline evidence and semantic diff baseline distinct but cross-checked.
- Remove dead release CLI flags.
- Make collection status resolve the actual collection manifest location.
- Establish one product version source.
- Bind release manifests to baseline evidence.
- Align active pipeline documentation with the V3 CLI.

## Exit criteria

- `registered = materialized + intentional_unmaterialized` for a fully covered V1 catalogue.
- No intentional entry is double-counted.
- `diff.baseline_present=true` without `data/baseline/latest.json` is a hard evidence error.
- Release manifest contains a digest for `metrics/baseline-evidence.json`.
- `--force` is not accepted by the promotion CLI.
- Publish status reads `backup/<date>/manifests/_collection.json`.
- `VERSION`, `src.engine.__version__`, and Semantic IR `engine_version` agree.
- Documentation no longer references the deleted V2 `scripts/pipeline.py` entry point.

## Non-goals

- V1 runtime cutover.
- Service model consolidation.
- Legacy deletion.
- New service materialization.

Those belong to Phases 1–8.
