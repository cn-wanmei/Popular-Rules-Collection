# Branch Protection — Recommended Required Checks

> **Status: Current settings guide**  
> Apply in GitHub → Settings → Branches → `main` rule.  
> This file is **not** enforced by API in this cycle (avoid overwriting existing protection).

## Popular-Rules-Collection

### PR merge into `main` (default)

Enable **Require status checks to pass** and select:

| Check name (workflow `name:`) | Why |
|-------------------------------|-----|
| `Unit Tests` | Architecture + engine unit/contract |
| `Directory Gate` | Tree invariants |
| `Engine v3 Independent Kernel` | Independent kernel gates |

Optional but recommended for source-binding PRs:

| Check name | When |
|------------|------|
| `Source Upstream Gate` | Handoff / immutable binding PRs |

Do **not** require:

- `Generated Status` / soft docs
- `Client GitHub Release Packages` (manual only)
- `Ecosystem Status (Read Model)` (read model, not merge gate)
- `Published Raw E2E` (post-publish consumer check)

### Settings toggles (recommended)

- Require a pull request before merging: **ON**
- Require status checks to pass before merging: **ON**
- Require branches to be up to date: optional (strict)
- Do not allow bypassing the above settings: per org policy

## Popular-Rules-Source

| Check name | Why |
|------------|-----|
| `CI` | validate.yml gate |

## Popular-Rules-Icon

`main` was **unprotected** at last audit. Minimum:

| Check name | Why |
|------------|-----|
| `PR CI (L0–L1)` | Existing PR gate |

Identity Freshness is scheduled/manual — **not** a merge required check.

## Related

- `docs/WORKFLOWS.md` — full inventory
- `docs/PHASE_G_PROGRESS.md` — completion tracker
