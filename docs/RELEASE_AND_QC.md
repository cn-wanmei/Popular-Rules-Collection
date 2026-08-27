# Release Definition & Quality Control (locked 2026-08-27)

## Status

**规则生成已达到可发布/可使用标准；规则数据治理进入持续质量控制阶段。**

| Layer | Status |
|-------|--------|
| Collect → Normalize → Canonical → Builder ×7 | ✅ structural validation |
| Generated client outputs | ✅ production-usable |
| Semantic / historical validation | ✅ P1-0…P1-3 + engineering P0–P2 |

Authoritative artifacts: `generated/{client}/` on `main`.  
Do **not** hand-edit `rule/`.

---

## Daily Service Coverage (definition)

**Goal is not “every brand name has its own ruleset file”.**

A popular daily service is **covered** when any of:

1. **Materialized** — dedicated rules in `database/` + `generated/{client}/`
2. **Aggregate-covered** — parent ecosystem ruleset is sufficient (e.g. Taobao → Alibaba, Drive → Google)
3. **Intentional-unmaterialized** — listed in `config/intentional_unmaterialized.yaml` with a reason code

```text
Daily Coverage = (materialized + intentional_unmaterialized) / registered
```

Raw `coverage` (materialized / registered) remains for engineering; **daily_coverage** is the product KPI.

### Service expansion gate (P2-4)

New Service requires **all** of:

1. Clear user value beyond an existing aggregate
2. Verified public upstream (BM / MetaCubeX / equivalent)
3. Registry path HTTP 200 at registration time
4. Identity tokens if BM Clash `# NAME:` is non-obvious

Otherwise: intentional entry only — **no fake domains**.

---

## Production use

1. Subscribe to `generated/{mihomo|sing-box|surge|shadowrocket|quantumult-x|egern|loon}/{id}.*`
2. GitHub Raw is source of truth; CDN is acceleration only
3. Typical interval: 86400s
4. Only **materialized** services resolve; intentional means “not a gap, no dedicated file by design”

### KPI (quality ≠ line count)

- **Daily coverage** & materialization rate  
- Source Health split: `configured` / `enabled` / `collected_this_run` / `historical_in_health`  
- Builder Coverage (**×7**, including Loon)  
- Validation (`schema_validate` / `validate` / `builder_validate` = pass|fail)  
- Identity warnings / Rule-count drift / Quality flags (soft)

`domain` vs `domain_suffix` stay distinct in the Canonical loader.

### Intentional unmaterialized

SSOT: **`config/intentional_unmaterialized.yaml`**

| code | meaning |
|------|---------|
| `NO_UPSTREAM` | no verified dedicated ruleset |
| `COVERED_BY_AGGREGATE` | use parent ecosystem rules |
| `MAPS_TO` | alias of another service id |
| `DEFERRED_PROFILE` | profile intentionally postponed |
| `KEYWORD_ONLY` | no usable domain set |
| `SOURCE_DRIFT` | upstream path moved; pending registry fix |

---

## Release metadata semantics

`reports/latest_release.json` (and `reports/<date>/release.json`):

| field | meaning |
|-------|---------|
| `commit` | **pipeline input SHA** when `release_snapshot.py` ran (before collect’s git commit) |
| `commit_role` | always `pipeline_input` |
| `validation.*` | `pass` / `fail` / `unknown` from gate artifacts |

After collect pushes, **HEAD advances by one commit** that *contains* this release file.  
Therefore `latest_release.commit` may lag `HEAD` by one pipeline commit — **by design**, not drift.

Do not treat `latest_release.commit == HEAD` as a hard requirement unless a post-commit rewrite job is added.

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

### Primary: Collect Upstream (`collect.yml`)

```text
Upstream → collect → normalize → database/
  → rule_loader → build ×7 (incl. loon) → generated/
  → schema_validate (hard, writes schema_validate.json)
  → validate (hard, writes validation_report.json)
  → builder_validate (hard)
  → identity / drift / quality (soft)
  → statistics → release_snapshot → …
  → commit → git pull --rebase → push
```

### Optional: Build Client Rules (`build.yml`)

Standalone rebuild of `generated/`. Must also run **Builder ×7 including Loon**, then:

```text
build ×7 → schema_validate → validate → builder_validate → commit
```

### Secondary: Validate workflow

Triggers on **Build Client Rules** and **Collect Upstream** completion, plus PR / manual.

Hard gates stay fail-closed. Soft QC never hides Source Health degradation.

---

## QC modules

| ID | Module | Behavior |
|----|--------|----------|
| **P1-0** | `schema_validate.py` | `id==filename`, canonical types — **hard** + JSON artifact |
| **P1-1** | `identity_validate.py` | BM `# NAME:` tokens — **soft** |
| **P1-2** | `rule_count_drift.py` | ±20/50/80% vs prior day — **soft** |
| **P1-3** | `quality_validate.py` / validate domain quality | bare TLD / empty generated / large sets — **soft** |
| **P0** | `build.yml` Loon + pre-commit validate | contract = ×7 |
| **P0** | `release_snapshot` real validation | no long-lived `unknown` when artifacts exist |

### Non-goals

- ❌ Builder / rule_loader / Primary rewrites for coverage optics  
- ❌ Collector path fuzzy matching  
- ❌ Fake upstream for intentional_unmaterialized  
- ❌ Mega service dumps without upstream audit  

---

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
