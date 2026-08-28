# Release & QC — Popular Rules Collection

## Release Candidate standard

```text
Service Coverage (Daily) ≥ 90% of target daily services
Source Health (enabled)  ≥ 95% when upstream reachable
Builder Coverage         100% (×7 clients)
Validation Errors        0
Schema Errors            0
Generated Empty          0
Stale Files              0
Broken Links             0
```

Source health distinguishes `healthy` / `degraded` / `blocked`. Occasional upstream 404 is **not** project failure.

## Daily Coverage (user-facing)

Do **not** report raw `materialized/registered` as “missing coverage”.

```text
Daily Coverage =
  (materialized + intentional_unmaterialized) / registered
```

Intentional codes (SSOT: `config/intentional_unmaterialized.yaml`):

| Code | Meaning |
|------|---------|
| `NO_UPSTREAM` | no verified dedicated ruleset |
| `COVERED_BY_AGGREGATE` | covered by parent ecosystem rules |
| `MAPS_TO` | alias of another service id |
| `DEFERRED_PROFILE` | profile intentionally postponed |
| `KEYWORD_ONLY` | keyword-only / empty domain set by design |
| `SOURCE_DRIFT` | upstream path moved; pending re-bind |

**No fake domains** for intentional entries.

## Expansion criteria

Only materialize when:

1. Verified upstream HTTP 200 with non-empty rules
2. Primary mapping exists **before** registry append
3. Not better expressed as aggregate coverage

## Release commit semantics

`reports/latest_release.json` `commit` is **pipeline_input** SHA (snapshot before collect commit). HEAD after push contains the snapshot and may differ by one commit — by design.

## Soft QC (P1)

| Gate | Script |
|------|--------|
| P1-1 | `identity_validate.py` |
| P1-2 | `rule_count_drift.py` |
| P1-3 | `quality_validate.py` |

## Engineering changelog (P0–P2, 2026-08-27)

| ID | Change |
|----|--------|
| P0-1 | `build.yml`: add `build_loon.py` |
| P0-2 | `release_snapshot` + gate JSON artifacts; commit semantics documented |
| P0-3 | Daily Coverage definition locked in this doc |
| P1-1 | `build.yml`: validate before commit |
| P1-2 | `validate.yml`: also on Collect Upstream |
| P1-4 | quality: empty generated + large-set hints |
| P2-1 | statistics: configured / enabled / collected / historical |
| P2-2 | intentional `code` enum |
| P2-3 | unexpected_missing → intentional entries |
| P2-4 | expansion gate above |

---

## Long-running production-grade bar

After identity + drift signals have been observed across ≥2 weeks of upstream noise, with BM-class drift still fixed via explicit registry edits only.

## Phase 2B-IP (2026-08-28)

Domain and IP tracks are **separate**:

- Domain: whitelist materialization only with verified upstream.
- IP: `sources/ip_registry.yaml` + `scripts/collect_ip.py` + `scripts/ip_cidr.py`.
- Hard rule: provider/CDN ranges must not be attributed to product services.
- See `docs/IP_ARCHITECTURE.md`.
