# Icon Pipeline — Week 2 / Week 3

## C2 Clarity retarget
- `quality-audit`: incomplete 8/8 + low_res → `retarget_services`
- `seed-audit`: bitmap embed / empty seed check
- Workflow: **Icon Quality Retarget** (batch rebuild with `--refresh`)

Note: current production “low_res” rows are mostly **missing variants** (0/8), not soft 16px favicons.

## C3 Renderer pointer
- `sync-pointer` aligns `release-pointer.json` to registry `renderer_version` (v5.1.0)
- Production pointer synced to **prc-icon-renderer-v5.1.0**

## D / metrics
- gap-fill emits `build/gap-fill-metrics.json`
- Retarget emits `acquisition-metrics.json` + audits as artifacts
- Full acquire/render process split remains sequential in one build for correctness; source cache + CAS enable future hard split
