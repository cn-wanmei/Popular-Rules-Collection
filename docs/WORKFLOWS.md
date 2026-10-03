# Workflow Classification

> **Status: Current**  
> Purpose: reduce Actions surface ambiguity. This is an **operator index**, not a fourth SSOT.
>
> Live numbers and pass/fail always come from CI runs and `PUBLISH_STATUS.md`.

## Layers

| Layer | Meaning |
|-------|---------|
| **PRODUCTION** | Moves or seals product state (collect, build, publish, handoff, user release) |
| **GATE** | Required checks for merge or publish integrity |
| **NON-PRODUCTION** | Status, docs, historical / diagnostic |

### Production authority

| Workflow (name pattern) | Production authority | Required for merge | Required for publish |
|-------------------------|----------------------|--------------------|----------------------|
| Collect Upstream | YES | No | Indirect (feeds build input) |
| Build Client Rules | YES | No | YES (candidate) |
| Publish Release Candidate | YES | No | YES |
| Source Auto Handoff | YES (binding PR) | No | No |
| Client GitHub Release Packages | YES (user zip) | No | No (manual only) |

### Gates

| Workflow (name pattern) | Production authority | Required for merge | Required for publish |
|-------------------------|----------------------|--------------------|----------------------|
| Validate / Unit Tests | NO | YES (typical) | Often |
| Directory Gate | NO | YES | Often |
| Engine v3 Independent Kernel | NO | YES | Often |
| Source Upstream Gate | NO | YES (handoff PRs) | Yes when binding |
| Source Canary | NO | Policy-dependent | Policy-dependent |
| Service / Production Hard Gate | NO | Policy-dependent | Policy-dependent |

### Non-production

| Workflow (name pattern) | Notes |
|-------------------------|-------|
| Generated Status / status.yml | Refreshes `PUBLISH_STATUS.md` |
| Documentation Layer | Soft / secondary after publish |
| Historical migration / audit | Historical = YES; not publish authority |

## Operator rule

```text
If unsure which run matters:
  1. Publish + Build = production path
  2. Required status checks on the PR = merge path
  3. action_required with zero jobs = noise; do not treat as authority
```

## Related

- `docs/RELEASE_RUNBOOK.md`
- `docs/ACTIONS_SHA_PIN.md`
- `docs/SOURCE_COLLECTION_FUNNEL.md`
