# Client GitHub Release package timing (P1)

Build/Publish success does **not** create user zip packages (by design).

| Stage | Trigger |
|-------|---------|
| Collect / V3 / Build / Publish | automated CI |
| Client GitHub Release Packages | manual `workflow_dispatch` on `client-github-release.yml` |
| Icon style packages | manual `workflow_dispatch` on Icon repo |

## Alignment recommendation

1. After a successful **Publish** promote, operator runs client package workflow within 24h if users consume Releases.
2. Optional: add badge on README / PUBLISH_STATUS showing **last package tag time** vs **last promote run_id**.
3. Do **not** auto-release every promote (noise + large assets).

See `docs/RELEASE_RUNBOOK.md` and Collection README Release section.
