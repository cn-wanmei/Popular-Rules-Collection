# Workflow Classification

> **Status: Current**  
> Operator index only — **not** a fourth SSOT.  
> Live pass/fail and numbers: CI runs + `PUBLISH_STATUS.md`.

## Layers

| Layer | Meaning |
|-------|---------|
| **PRODUCTION** | Moves or seals product state |
| **GATE** | Integrity checks (merge / publish policy) |
| **NON-PRODUCTION** | Status, docs, audit / diagnostic |

---

## Inventory (Collection `.github/workflows/`)

| File | Layer | Production authority | Typical required for merge | Notes |
|------|-------|----------------------|----------------------------|-------|
| `collect.yml` | PRODUCTION | YES | No | Upstream collect → backup |
| `build.yml` | PRODUCTION | YES | No | Builds RC (candidate) |
| `publish.yml` | PRODUCTION | YES | No | Atomic publish of exact RC |
| `source-auto-handoff.yml` | PRODUCTION | YES (opens binding PR) | No | Collection-owned handoff |
| `post-handoff-binding-sync.yml` | PRODUCTION | YES (alignment PR) | No | After handoff merge |
| `client-github-release.yml` | PRODUCTION | YES (user zips) | No | **workflow_dispatch only** |
| `validate.yml` | GATE | NO | **YES** | Schema / icon samples / gates |
| `test.yml` | GATE | NO | **YES** | Unit tests |
| `directory-gate.yml` | GATE | NO | **YES** | Tree invariants |
| `engine-v3.yml` | GATE | NO | **YES** | Independent kernel |
| `source-upstream-gate.yml` | GATE | NO | **YES** on handoff PRs | Lineage / registry |
| `source-canary.yml` | GATE | NO | Policy | Canary promotion path |
| `service-completion-gate.yml` | GATE | NO | Policy | Service completeness |
| `service-production-gate.yml` | GATE | NO | Policy | Production unlock |
| `status.yml` | NON-PRODUCTION | NO | No | Refreshes `PUBLISH_STATUS.md` |
| `docs.yml` | NON-PRODUCTION | NO | No | Soft docs layer |
| `audit.yml` | NON-PRODUCTION | NO | No | Diagnostic |
| `rule-mapping-release.yml` | NON-PRODUCTION / special | NO | No | Mapping release path |
| `ecosystem-status.yml` | NON-PRODUCTION | NO | No | Cross-repo read model |
| `published-raw-e2e.yml` | NON-PRODUCTION | NO | No | Consumer raw check |

---

## Required-check guidance

See **[`docs/BRANCH_PROTECTION.md`](BRANCH_PROTECTION.md)** for Settings UI steps.

### Default merge path (PR into `main`)

```text
Unit Tests
Directory Gate
Engine v3 Independent Kernel
```

Handoff / binding PRs additionally:

```text
Source Upstream Gate
```

### Publish path

```text
Build Client Rules  →  Publish Release Candidate
```

### Operator rule

```text
1. Publish + Build = production path
2. Required status checks on the PR = merge path
3. action_required with zero jobs = noise
4. Do not add a new gate.yml without retiring a duplicate
```

---

## Related

- `docs/BRANCH_PROTECTION.md`
- `docs/RELEASE_RUNBOOK.md`
- `docs/ACTIONS_SHA_PIN.md`
- `docs/SOURCE_COLLECTION_FUNNEL.md`
- `docs/PHASE_G_PROGRESS.md`
