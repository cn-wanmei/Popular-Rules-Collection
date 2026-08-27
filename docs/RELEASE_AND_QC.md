# Release Definition & Quality Control (locked 2026-08-27)

## Status

**规则生成已达到可发布/可使用标准；规则数据治理进入持续质量控制阶段。**

| Layer | Status |
|-------|--------|
| Collect → Normalize → Canonical → Builder ×7 | ✅ structural validation |
| Generated client outputs | ✅ production-usable |
| Semantic / historical validation | ✅ P1-0…P1-3 landed (soft) |

Authoritative artifacts: `generated/{client}/` on `main`.  
Do **not** hand-edit `rule/`.

---

## Production use

1. Subscribe to `generated/{mihomo|sing-box|surge|shadowrocket|quantumult-x|egern|loon}/{id}.*`
2. GitHub Raw is source of truth; CDN is acceleration only
3. Typical interval: 86400s
4. Only **materialized** services resolve; see intentional unmaterialized

### KPI (quality ≠ line count)

- Service / Ecosystem coverage & materialization rate  
- Source Health (`healthy` / `degraded`, `files_ok` / `files_failed`)  
- Builder Coverage (×7)  
- Validation (schema / validate / builder_validate)  
- Identity warnings / Rule-count drift / Quality flags (soft)

`domain` vs `domain_suffix` stay distinct in the Canonical loader.

### Intentional unmaterialized

```text
Primary ✓  +  Registry ✗  →  intentional_unmaterialized
reason: no_verified_upstream
```

| id | note |
|----|------|
| mistral / gcp / supabase | no verified upstream |
| roblox / minecraft | no BM / MetaCubeX path (2026-08-27) |
| blizzard | maps to battlenet |

---

## Fault taxonomy

| Layer | Meaning |
|-------|---------|
| Primary ✗ | not planned |
| Primary ✓ / Registry ✗ | intentional_unmaterialized |
| Registry ✓ / Upstream ✗ | **registry drift** — fix path explicitly |
| Upstream ✓ / Database ✗ | collect / normalize |
| Database ✓ / Generated ✗ | builder |
| Generated ✓ / Validate ✗ | format / schema / expected-output |

Primary long-term risk: **Source Drift**, not Builder.

---

## Pipeline

```text
Upstream → collect → normalize → database/
  → rule_loader → build ×7 → generated/
  → schema_validate (P1-0) → validate (P1-3 quality warns)
  → builder_validate
  → identity_validate (P1-1 soft) → rule_count_drift (P1-2 soft)
  → statistics → generate_rule_pages --strict → size_gate
  → commit → git pull --rebase origin main → push
```

Hard gates stay fail-closed. Soft QC never hides Source Health degradation.

---

## QC P1 (implemented)

| ID | Module | Behavior |
|----|--------|----------|
| **P1-0** | `schema_validate.py` | `id==filename`, canonical types, non-empty values — **hard** |
| **P1-1** | `identity_validate.py` + `config/identity_hints.yaml` | BM `# NAME:` vs expected tokens — **soft** |
| **P1-2** | `rule_count_drift.py` | per-service ±20/50/80% vs prior day — **soft** |
| **P1-3** | `validate.py` `domain_quality_issues` | bare TLD / ultra-short / pathological — **soft** |

### Non-goals

- ❌ Builder / rule_loader / Primary rewrites for coverage optics  
- ❌ Collector path fuzzy matching  
- ❌ Fake upstream for intentional_unmaterialized  
- ❌ Mega service dumps (50–100) without upstream audit  

---

## Gaming expansion (2B-4)

| id | upstream | status |
|----|----------|--------|
| garena | BM `rule/Clash/Garena/Garena.yaml` | registered (materialize on next collect) |
| roblox | — | intentional_unmaterialized |
| minecraft | — | intentional_unmaterialized |

---

## Long-running production-grade bar

After identity + drift signals have been observed across ≥2 weeks of upstream noise, with BM-class drift still fixed via explicit registry edits only.
