# Batch Status — 2026-08-27 (QC P1 complete)

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

## QC P1

| ID | Status |
|----|--------|
| P1-0 Rule schema | ✅ hard gate |
| P1-1 Identity | ✅ soft (`identity_validate.py`) |
| P1-2 Count drift | ✅ soft (`rule_count_drift.py`) |
| P1-3 Quality width | ✅ soft (`validate.py`) |

## Next (ops)

- Observe soft warnings for 1–2 weeks before promoting any to hard gate  
- Expand services only with verified upstream paths  
