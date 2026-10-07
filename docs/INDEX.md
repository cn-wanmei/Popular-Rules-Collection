# Documentation index (Collection)

## Start here
- [Root README](../README.md)
- [PUBLISH_STATUS.md](../PUBLISH_STATUS.md) — CI-generated live status (not hand-written)
- [rule/_index.yaml](../rule/_index.yaml) — **Canonical service identity SSOT**
- [generated/manifest.json](../generated/manifest.json) — machine client distribution manifest
- [SERVICE_CATALOG.generated.md](SERVICE_CATALOG.generated.md) — **current** generated service catalog

## User / consumer
- [RULE_USAGE_GUIDE.md](RULE_USAGE_GUIDE.md) — usage patterns (see banner: dynamic numbers → SSOT)
- [GENERATED_OUTPUTS.md](GENERATED_OUTPUTS.md) — client output layout
- [NETWORK_USAGE.md](NETWORK_USAGE.md)

## Architecture
- [ARCHITECTURE.md](ARCHITECTURE.md)
- [STATE_MODEL.md](STATE_MODEL.md) — Lifecycle × Freshness × Health × Lineage
- [PRODUCTION_RULE_CHAIN.md](PRODUCTION_RULE_CHAIN.md)
- [ROUTING_CONTRACT.md](ROUTING_CONTRACT.md)
- [ICON_V6_CUTOVER.md](ICON_V6_CUTOVER.md)

## Operations / release
- [WORKFLOWS.md](WORKFLOWS.md)
- [RELEASE_RUNBOOK.md](RELEASE_RUNBOOK.md)
- [DISASTER_RECOVERY.md](DISASTER_RECOVERY.md)
- [BRANCH_PROTECTION.md](BRANCH_PROTECTION.md)
- [SSOT_NUMBERS.md](SSOT_NUMBERS.md) — where numbers live (README must not invent them)
- [FUNNEL_OPS.md](FUNNEL_OPS.md) — Source health degraded + weekly canary quota
- [LEGACY_STATUS.md](LEGACY_STATUS.md) — `database/` deletion gate status
- [RELEASE_PACKAGE_TIMING.md](RELEASE_PACKAGE_TIMING.md) — user GitHub Release packages vs promote
- [RETENTION_ENFORCEMENT.md](RETENTION_ENFORCEMENT.md) — retention hard schedule checklist

## Documentation Layer
- [Schema / contract](schema/DOCUMENTATION_SPEC.yaml)
- [docs-index.json](generated/docs-index.json)
- Service pages: `docs/services/**` · `docs/rules/{id}.md`
- Path links: [PATH_LINKS_G3.md](schema/PATH_LINKS_G3.md) · [`rule/`](../rule/) · [`generated/`](../generated/)

## Related repos
- [Popular-Rules-Source](https://github.com/cn-wanmei/Popular-Rules-Source) — Evidence supply
- [Popular-Rules-Icon](https://github.com/cn-wanmei/Popular-Rules-Icon) — Icon assets

## Historical / archive
- [SERVICE_CATALOG.md](SERVICE_CATALOG.md) — **historical snapshot entry** (prefer `.generated.md`)
- [archive/activation/](archive/activation/)
- [archive/ROOT_STUBS.md](archive/ROOT_STUBS.md) — root freeze stubs (removed on this branch)
- [archive/ARCHIVE_INVENTORY.md](archive/ARCHIVE_INVENTORY.md) — phase/p0 config move inventory
- [archive/icon-v5/](archive/icon-v5/)
- [archive/phases/](archive/phases/)
- [schemas/archive/icon-v5/](../schemas/archive/icon-v5/)

> Phase / date-stamped planning docs not listed here are historical. Prefer SSOT configs and CI status over narrative status tables.
