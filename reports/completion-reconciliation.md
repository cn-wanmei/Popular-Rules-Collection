# Completion Reconciliation Report

Generated: `2026-09-28T06:21:57.780848+00:00`

## Snapshot

| Metric | Count |
|--------|------:|
| Active immutable bindings | 281 |
| Rule index services | 394 |
| Active not in rule index | 1 |

Active missing from index: `baidu`

## Core subtree status

| Provider | Hierarchy children | Planned discovery |
|----------|-------------------:|-------------------|
| tencent | 16 | qqzone, tenpay, tencentads, tencentmap, wetype, sogou |
| bytedance | 10 | pipixia, fanqie, dongchedi, oceanengine |
| alibaba | 15 | quark, uc, hema, taobaolive |
| google | 35 | googleworkspace, googlemeet, googlechat, googlecalendar, googletranslate |
| microsoft | 22 | microsoft365, dynamics, powerautomate, powerapps, visualstudio |

## Notes

- Durable main-node seal ≈ complete; remaining work is subtree ownership split + hostname evidence.
- Company-root seed ≠ full subtree coverage.
- Invariant: handoff → Collect → Build → Publish.
