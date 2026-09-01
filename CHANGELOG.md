# Changelog

## [1.0.1] — 2026-09-01

### Engine v3 Independent Kernel (Stabilization)

**Status:** RC → Independent production kernel foundation  
**V2 Runtime Dependency:** **0**

#### Breaking / Architecture
- Completely cut V2 runtime dependency from the Engine production path.
- `database/services` is no longer a runtime input. It may only be consumed once via `migrate-legacy` to produce a Source Snapshot.
- Pipeline order is now hard-enforced:
  ```
  snapshot → ingest → quarantine → canonical
  → hierarchy → ir → adapters → diff → golden → release
  ```
- All build artifacts are isolated under `data/runs/<run_id>/` (atomic workspace).
- Publish / promotion only allowed when Release State == `RC_READY`.

#### Added
- `src/engine/ingest/` — Source Snapshot ingest (V2-free)
- `src/engine/ingest/migrate_legacy.py` — one-time bridge from `database/services`
- `src/engine/snapshot/` — immutable Source Snapshot
- `src/engine/quarantine/` — quarantine **before** Canonical
- `src/engine/canonical/` — Canonical SSOT with error recording (no silent drop)
- `src/engine/hierarchy/` — Service / Group / Aggregate views
- `src/engine/decision/` — Decision SSOT (no `svcs[0]`, no substring heuristics)
- `src/engine/ir/` — full hierarchy + decisions in IR
- `src/engine/adapters/` — 7 native client adapters with correct extensions
- `src/engine/diff/` — unified path + safe baseline promotion
- `src/engine/golden/` — real L1–L7 semantic gates
- `src/engine/release/` — Release State Machine
- `src/engine/reproducibility/` — true hash digests + run compare
- `src/engine/promote/` — Artifact Promotion + Rollback
- `src/engine/cli/` — formal CLI (`python -m src.engine.cli`)
- `src/engine/validation/naming_gate.py` — permanent anti-v3-path / anti-V2-runtime gate
- `.github/workflows/engine-v3.yml` — CI for Engine gates
- `docs/engine/V3_INDEPENDENT_KERNEL.md`

#### Fixed (from 1.0.0 audit)
- Quarantine no longer runs after adapters
- Snapshot is no longer a post-build V2 oracle
- Diff path unified (`latest.json` + compatibility `differential.json`)
- Baseline promotion only after release success
- Rule IDs use full SHA-256 (64 hex)
- IR no longer truncates memberships or empties groups/aggregates
- Client artifacts use native extensions (sing-box `.json`, Egern `.yaml`, …)

#### CLI
```bash
python -m src.engine.cli all --sources ./sources --data ./data
python -m src.engine.cli migrate-legacy --database-services ./database/services
python -m src.engine.cli promote --run-id <id>
python -m src.engine.cli rollback --run-id <id>
python -m src.engine.cli reproducibility --run-a ... --run-b ...
```

#### Migration note
1. Run `migrate-legacy` once to freeze `database/services` into a Snapshot.
2. Subsequent builds use only Snapshots / Engine stages.
3. V2 build scripts under `scripts/build_*.py` remain for reference only and are not part of the Engine runtime.

---

## [1.0.0] — 2026-09-01 (prior)

- Initial Engine pipeline takeover (RC). Contained residual V2 runtime coupling that is removed in 1.0.1.
