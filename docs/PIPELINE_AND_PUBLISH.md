# Pipeline & Publish

> **Status: Current**  
> Authority: `docs/ARCHITECTURE.md` · `docs/PRODUCTION_RULE_CHAIN.md` · `PUBLISH_STATUS.md`  
> Historical V1/`rules/` semantics are retired; do not reintroduce them here.

## Current production entry points

```bash
python -m src.engine.cli all
python -m src.engine.cli naming_gate
python -m src.engine.cli promote --run-id <id>
python -m src.engine.cli rollback --run-id <id>
```

Manual GitHub Release packages (user zip) are **workflow_dispatch only** — see `docs/RELEASE_RUNBOOK.md`.

## Production flow

```text
upstream
  → immutable backup
  → V3 Engine
  → Canonical → Semantic IR
  → 7 Client Adapters + Network Dataset
  → gates
  → Release Candidate
  → atomic publish
  → generated/ + rule/
```

## Truth boundary

| Path | Role |
|------|------|
| `data/runs/<run-id>/canonical/` | V3 Canonical for that run |
| `data/runs/<run-id>/ir/` | Semantic IR |
| `rule/` | **Current** human browse / search / selection tree (from same IR as generated) |
| `generated/` | Client + network distributions |
| `sources/` | Upstream definitions + immutable binding |
| `database/services/` | Legacy evidence (not the live rule tree) |

### Directory invariants (must match Architecture)

- Exactly one human rule tree: **`rule/`**
- **`rules/` must not exist** and must not be recreated
- `rule/` is not copied from any client; neither `rule/` nor `generated/` is source for the other
- Legacy deletion is never automatic

## Publish semantics

- Build produces an immutable Release Candidate bound to Build Run ID + Head SHA
- Publish promotes that exact candidate to `main`
- Build / Publish success does **not** create a user GitHub Release

Authoritative live status: [`PUBLISH_STATUS.md`](../PUBLISH_STATUS.md) (CI-generated).
