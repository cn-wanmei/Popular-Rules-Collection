# CI Automation Inventory

## Active Production / Validation Workflows

| Workflow | Role |
|---|---|
| collect.yml | Scheduled Collection snapshot |
| build.yml | V3 immutable build, semantic/determinism/migration gates |
| publish.yml | Immutable artifact verification and atomic publication |
| test.yml | Repository + Engine regression |
| validate.yml | Registry/IP/Dataset/size validation |
| engine-v3.yml | V3 kernel gates |
| service-production-gate.yml | Service production hard gate |
| p0-service-gate.yml | P0 production status |
| p0-batch01-runtime-audit.yml | P0 runtime audit |
| phase-j-p0-50.yml | P0 50/50 progress gate |
| phase-m-dual-track.yml | Future dual-track readiness |
| phase-n-runtime-cutover.yml | Future runtime cutover |
| phase-o-observation-retirement.yml | Future observation / retirement |
| phase-o-r-operational-closure.yml | Future operational closure |
| directory-gate.yml | Canonical directory migration guard |
| v1-loader.yml | V1 loader contract |
| icons.yml | Service icon pipeline |
| retention.yml | Retention |
| status.yml | Status projection |
| audit.yml | Audit reporting |
| branch-cleanup.yml | Branch hygiene |

## Retired

The following completed Phase automation has been removed from active CI:

- phase-i-gate-closure.yml
- phase-k-intentional-final.yml
- phase-l-canonical-contract-freeze.yml
- phase8-closure-delete.yml

The associated completed phase scripts were also removed where no longer part of the active production path.

## Important

Retiring workflow automation does not delete historical reports, commits or PRs. History remains available in Git for audit.

## Rule

Only active gates that protect the current production boundary should execute automatically on main.
