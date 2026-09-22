# Documentation Architecture

Documentation is a derived human-facing view of V3 production state。

```text
V3 config + generated/manifest.json → docs/rules/*.md
```

Every service page must use current paths from `generated/manifest.json`. Legacy generated paths and `database/services/` are historical references only.

## SSOT
- Production DAG: `docs/PRODUCTION_RULE_CHAIN.md`
- Outputs: `docs/GENERATED_OUTPUTS.md`
- Routing: `docs/ROUTING_*.md`
- Icons: `docs/ICON_USAGE.md` + `assets/icons/v3/release-pointer.json`

Removed historical documentation generators are not current runtime dependencies。