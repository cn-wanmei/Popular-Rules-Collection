# Funnel / coverage dashboard (P2)

Lightweight operational read model (no extra service).

## Automated signals

| Signal | Where |
|--------|--------|
| Collection publish / health counts | `PUBLISH_STATUS.md` (CI) |
| Source lifecycle counts | Source `reports/generated/lifecycle.json` + README summary |
| Icon coverage | Icon `config/release-pointers.yaml` |
| Entity mix | `python scripts/entity_coverage_report.py` |
| Retention plan | workflow **Retention** artifact weekly |

## Weekly operator checklist

1. Source: `python -m source_engine health` → triage degraded (`docs/FUNNEL_OPS.md`)
2. Source: ≥8 VERIFIED→CANARY if quota due (`FUNNEL_ACCELERATION`)
3. Collection: note last promote vs last client package (`RELEASE_PACKAGE_TIMING.md`)
4. Icon: Identity Freshness green or open sync PR
5. Retention: review weekly dry-run artifact; apply only intentionally

## Trend (manual until dedicated job)

Store weekly note under `docs/archive/audits/funnel_YYYY-MM-DD.md` with:
- source state histogram
- entity_coverage_report JSON
- icon production release_id
