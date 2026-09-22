# Documentation Architecture

Documentation is a derived human-facing view of V3 production state.

```text
V3 config + rule/manifest.json + generated/manifest.json
                         ↓
                   docs/rules/*.md
```

`rule/` is the user-facing browse/search/selection distribution; `generated/` is the client and network distribution. Documentation may reference both, but neither is a documentation source of truth: Canonical and Semantic IR remain authoritative.

Every service page must use current paths and identities from the release manifests. Legacy generated paths and `database/services/` are historical references only.

## SSOT
- Production DAG: `docs/PRODUCTION_RULE_CHAIN.md`
- Outputs: `docs/GENERATED_OUTPUTS.md`
- Rule catalog: `docs/RULE_CATALOG.md`
- Routing: `docs/ROUTING_*.md`
- Icons: `docs/ICON_USAGE.md` + `assets/icons/v3/release-pointer.json`

Removed historical documentation generators are not current runtime dependencies.