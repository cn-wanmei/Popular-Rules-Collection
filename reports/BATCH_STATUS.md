# Batch Status — 2026-08-26

## Closed

| Batch | Scope | Result |
|-------|--------|--------|
| P0 | Builder freeze (rule_loader + mihomo/sing-box/surge + builder_validate) | ✅ |
| 1 | Core ecosystems (Tencent/Alibaba/ByteDance/Baidu/JingDong/Amazon/…) | ✅ |
| 2 | ChinaMobile/Unicom/Telecom + 12306 + UnionPay | ✅ |
| UnionPay audit | Bank ownership / aggregate semantic boundary | ✅ PASS |
| 3 | AI + Developer | ✅ |
| 4 | Gaming | ✅ (blizzard unmaterialized — upstream maps to battlenet) |
| 5 | Streaming / Social | ✅ |
| 6 | Long-tail (china/other/network/finance/privacy) | ✅ |

## Validation

```
builder_validate  failures=0 warnings=0
validate          Errors=0 Warnings=0
schema_validate   errors=0  (expected warnings: baidu, jingdong aggregate)
Source Health     100%
Builder Coverage  100%
```

## Metrics

```
Service Coverage     133 / 137
Materialization Rate ~97.1%
Rule Coverage        domains≈354,695  ips≈6,457
```

## Unmaterialized (registered, no invent)

| id | reason |
|----|--------|
| adblock-light | no_database_yaml (hagezi upstream available later) |
| adblock-pro | no_database_yaml |
| blizzard | no separate upstream (BM Blizzard → battlenet) |
| stripe | keyword-only / empty domain set |

## Architecture freeze

```
registry → collect → normalize → database
  → rule_loader (canonical)
  → Builder ×7 → generated/
  → generate_rule_pages --strict → rule/<PrimaryEcosystem>/<Service>/
```

CI (`collect.yml`) rebuilds database/generated/rule on schedule / workflow_dispatch.
