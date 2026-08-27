# Batch Status — 2026-08-27 (Phase 3A/3B locked · 3C ready)

## Release

See **`docs/RELEASE_AND_QC.md`**.

> 规则生成可发布/可使用；数据治理进入持续 QC。

## CI

| Item | Status |
|------|--------|
| Collect #19 | ✅ success |
| BM health | ✅ files_failed=0 |
| push race fix | ✅ pull --rebase |

## Phase 2B

| Step | Status |
|------|--------|
| 2B-1 JingDong / iQIYI drift | ✅ |
| 2B-2 Tier0 AI/Cloud | ✅ materialized where upstream exists |
| 2B-3 intentional_unmaterialized | ✅ |
| **2B-4 Gaming** | ✅ Garena registered; Roblox/Minecraft no upstream |

## Phase 3

| Step | Status |
|------|--------|
| **3A** Release snapshot / manifest / source snapshot | ✅ scripts + CI soft |
| **3B** intentional SSOT + lifecycle + identity/drift | ✅ config SSOT; stats now loads YAML |
| **3C** next batch (4–8 verified) | 📋 ready — see `reports/candidates/batch_3c_2026-08-27.md` |
| **3D** service_score v1 | ✅ scaffold (heuristic); multi-source agreement later |

### 3C candidate batch (verified BM 200)

`anthropic` · `digitalocean` · `atlassian` · `slack` · `line` · `kakaotalk` · `adobe` · `oracle`

### Fix applied

- `scripts/statistics.py` now loads `config/intentional_unmaterialized.yaml` as SSOT (was hardcoded 4 entries → 9).

## QC P1

| ID | Status |
|----|--------|
| P1-0 Rule schema | ✅ hard gate |
| P1-1 Identity | ✅ soft (`identity_validate.py`) |
| P1-2 Count drift | ✅ soft (`rule_count_drift.py`) |
| P1-3 Quality width | ✅ soft (`validate.py`) |

## Next (ops)

1. Append 8 registry rules → trigger collect  
2. Observe soft warnings 1–2 weeks before any hard-gate promotion  
3. Expand only with verified upstream paths  
