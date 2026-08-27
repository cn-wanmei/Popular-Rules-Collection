# Batch Status — 2026-08-27 (Phase 2B)

## Phase 2B SOP (locked)

```
Primary → Registry → Upstream → Materialize → Build ×7 → Validate
```

Fault taxonomy:
- Primary ✗ → 未规划
- Primary ✓ / Registry ✗ → intentional_unmaterialized (no_verified_upstream)
- Registry ✓ / Upstream ✗ → registry drift
- Upstream ✓ / Database ✗ → collect/normalize
- Database ✓ / Generated ✗ → builder
- Generated ✓ / Validate ✗ → format/schema

## Closed (Batch 1–6)

| Batch | Scope | Result |
|-------|--------|--------|
| P0 | Builder freeze | ✅ |
| 1–6 | Core / CN / AI / Gaming / Streaming / Long-tail | ✅ |
| UnionPay audit | Bank ownership boundary | ✅ PASS |

## Phase 2B in progress

| Step | Scope | Status |
|------|--------|--------|
| 2B-0 | HEAD audit (no Builder/Loader/Primary regression) | ✅ |
| **2B-1** | BM7 Registry drift: JingDong + iQIYI paths | ✅ commit `3cf41b7` |
| 2B-1.5 | Identity: HTTP 200 + NAME match + rules>0 | ✅ pre-CI (360buy* / iqiyi*) |
| 2B-0 CI | Full collect workflow_dispatch | 🔄 run 33044773318 |
| 2B-2 | Tier0 materialize: perplexity/groq/xai/aws/firebase | ⏳ after CI |
| 2B-3 | intentional_unmaterialized: mistral/gcp/supabase | ⏳ document only |
| 2B-4 | Roblox / Minecraft expansion | 🚫 after 2B-0–2B-2 green |

### 2B-1 path fixes

| service | old path | new path |
|---------|----------|----------|
| jingdong | `rule/Clash/JD/JD.yaml` (404) | `rule/Clash/JingDong/JingDong.yaml` |
| iqiyi | `rule/Clash/iQiyi/iQiyi.yaml` (404) | `rule/Clash/iQIYI/iQIYI.yaml` |

No Collector fuzzy matching. Registry is path source of truth.

### Intentional unmaterialized (terminology)

Use `intentional_unmaterialized` + `reason: no_verified_upstream` — **not** "blocked".

| id | primary | registry | reason |
|----|---------|----------|--------|
| mistral | ✓ | ✗ | no_verified_upstream |
| gcp | ✓ | ✗ | no_verified_upstream |
| supabase | ✓ | ✗ | no_verified_upstream |
| blizzard | ✓ | maps→battlenet | no separate upstream |

### NetEase note

`NetEaseMusic` path is valid; semantic scope is music-only. Keep until explicit product decision for full `NetEase` ecosystem.

## Do not

- Change Builder / rule_loader / Primary architecture
- Auto path fuzzy match in Collector
- Invent sources for mistral/gcp/supabase
- Expand 50–100 services in one batch
