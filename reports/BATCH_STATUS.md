# Batch Status — 2026-08-27 (Phase 2B QC locked)

## Release definition (locked)

See **`docs/RELEASE_AND_QC.md`**.

> 规则生成已达到可发布/可使用标准；规则数据治理进入持续质量控制阶段。

## CI snapshot

| Item | Status |
|------|--------|
| Collect run #19 | ✅ success |
| BM health | ✅ `files_ok=95` `files_failed=0` healthy |
| JingDong / iQIYI path fix | ✅ in registry + re-collected |
| Commit race (`pull --rebase`) | ✅ workflow fixed |

## Phase 2B

| Step | Status |
|------|--------|
| 2B-0 HEAD / no Builder regression | ✅ |
| 2B-1 Registry drift JingDong + iQIYI | ✅ |
| 2B-1.5 Identity pre-check | ✅ |
| 2B-0 full CI after fix | ✅ #19 |
| 2B-2 Tier0 materialize audit | ✅ (perplexity/groq/xai/aws/firebase present) |
| 2B-3 intentional_unmaterialized | ✅ mistral/gcp/supabase (no fake sources) |
| 2B-4 Roblox/Minecraft | ⏳ optional expansion after QC P1-0 |

## QC P1 (post-release)

| ID | Scope | Status |
|----|--------|--------|
| P1-0 | Rule schema test in schema_validate | ✅ landed |
| P1-1 | Source → Service identity | 📋 next |
| P1-2 | Rule count drift | 📋 planned |
| P1-3 | Abnormal width / quality warnings | 📋 planned |

## Do not

- Change Builder / rule_loader / Primary for coverage optics
- Collector path fuzzy matching
- Invent upstream for intentional_unmaterialized
- Mega-batches of 50–100 services
