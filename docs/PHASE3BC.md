# Phase 3B / 3C

## 3B — Coverage & Missing Audit

| Script | Output |
|--------|--------|
| `coverage_matrix.py` | `coverage.json`, `coverage.md`, `latest_coverage.json` |
| `hot_missing_audit.py` | `HOT_MISSING_SERVICES.md`, `hot_missing.json` |

## 3C — Provider IP Expansion

| Artifact | Path | Rule |
|----------|------|------|
| Cloudflare / AWS | `database/provider/` | **Provider ≠ Service** |
| Export | `generated/provider/` | Not merged into product service lists |

`collect_providers` refuses `database/ips/` paths.
