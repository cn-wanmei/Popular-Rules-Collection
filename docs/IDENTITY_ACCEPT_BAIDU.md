# Identity Accept: baidu

## Facts (2026-10-08)

| Layer | State |
|-------|--------|
| Source `baidu` | `verified`, enabled |
| Collection `rule/baidu/baidu/baidu.yaml` | **`entity: provider_aggregate`** (354 DOMAIN_SUFFIX) |
| Collection services under provider baidu | baidu-zhidao, baidumaps, baidunetdisk, baidutieba, baiduwenku, … |

## Why not auto-flip to `entity: service`

`provider_aggregate` is intentional for broad Baidu domain set. Source `baidu` verified does **not** mean Collection must rename aggregate → service without:

1. Evidence that a **service-scoped** canonical node is required for routing/icon/handoff
2. Overlap audit vs child services
3. Icon registry impact (coverage is entity:service only)

## Accept checklist

- [ ] Decide product shape: keep aggregate **or** add `baidu-core` service + keep aggregate
- [ ] Source seal binding in `immutable_registry`
- [ ] Icon identity only if new `entity: service` id
- [ ] No bulk domain move without semantic gate

Until then: **no automatic entity change**.
