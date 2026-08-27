# Release Definition & Quality Control (locked 2026-08-27)

## Status

**规则生成已达到可发布/可使用标准；规则数据治理进入持续质量控制阶段。**

| Layer | Status |
|-------|--------|
| Collect → Normalize → Canonical → Builder ×7 | ✅ structural validation in place |
| Generated client outputs | ✅ usable for production routing |
| Semantic / historical validation | 🔄 Phase 2B QC (P1) |

Authoritative artifacts: `generated/{client}/` on branch `main`.
Do **not** hand-edit `rule/` (generated product pages).

---

## Production use

1. Subscribe to `generated/{mihomo|sing-box|surge|shadowrocket|quantumult-x|egern|loon}/{id}.*`
2. Prefer GitHub Raw as source of truth; CDN mirrors are acceleration only
3. Update interval: typically 86400s
4. Only **materialized** services are expected to resolve; see intentional unmaterialized below

### KPI (quality, not raw rule count)

- Service Coverage / Materialization rate
- Ecosystem Coverage
- Source Health (`healthy` vs `degraded`, `files_ok` / `files_failed`)
- Builder Coverage (7 clients)
- Validation (schema / validate / builder_validate)

**Not a KPI:** “more domain lines is better.”  
`domain` and `domain_suffix` remain distinct in the Canonical loader — do not merge for prettier dedup counts.

### Intentional unmaterialized

```text
Primary ✓  +  Registry ✗  →  intentional_unmaterialized
reason: no_verified_upstream
```

Examples: `mistral`, `gcp`, `supabase`. Do not invent fake registry sources for coverage optics.

---

## Fault taxonomy (five layers)

| Layer | Fail means |
|-------|------------|
| ① Primary ✗ | Service not planned |
| ② Primary ✓ / Registry ✗ | intentional_unmaterialized / no_verified_upstream |
| ③ Registry ✓ / Upstream ✗ | **registry drift** (fix path explicitly; never fuzzy-match in Collector) |
| ④ Upstream ✓ / Database ✗ | collect / normalize defect |
| ⑤ Database ✓ / Generated ✗ | builder defect |
| ⑥ Generated ✓ / Validate ✗ | format / schema / expected-output |

Primary long-term risk is **Source Drift**, not Builder regression.

---

## Pipeline (structural)

```text
Upstream → collect → normalize → database/
  → rule_loader (canonical)
  → build ×7 → generated/
  → schema_validate → validate → builder_validate
  → generate_rule_pages --strict → size_gate → commit
```

Hard gates must stay fail-closed. Soft: statistics / docs / links.

Commit step must `git pull --rebase origin main` before `git push` to absorb concurrent main updates.

---

## Phase 2B QC roadmap (do not expand Builders)

Focus shifts from “how many services” to “stable, trusted, maintainable.”

### P1-0 Rule Schema Test — **in progress**

Every `database/services/{id}.yaml`:

- `id` present and `id == filename stem`
- `rules` is a list (may be empty when domains/ips sidecars hold bulk data)
- each rule: `type ∈ canonical types`, `value` non-empty

Implemented in `scripts/schema_validate.py` (hard errors on corrupt rows).

### P1-1 Source → Service Identity

HTTP 200 ≠ correct service identity.

Plan:

- Optional registry field: `identity: { service: <id> }` or `expected_name`
- Validator checks upstream markers / sample domains after collect
- Start as **warnings**; promote to gate only after low false-positive rate
- Never auto-guess paths in Collector

### P1-2 Rule Count Drift

Silent collapse example: OpenAI 101 → 7 with validate still green.

Plan:

- Per-service baseline in `reports/rule_counts/` (or summary history)
- Thresholds (default, non-Error): ±20% warn · ±50% high · ±80% review
- Tunable per large natural-volatility sets (adblock, china)

### P1-3 Rule Quality / abnormal width

Beyond format checks in `validate.py`:

- Extreme short suffixes, bare TLD, pathological wildcards, absurd CIDR
- Start as **warnings + report**; avoid hard-fail false kills

### Explicit non-goals (this phase)

- ❌ Change Builder / rule_loader / Primary architecture for coverage optics
- ❌ Collector path fuzzy matching
- ❌ Fake upstream for mistral/gcp/supabase
- ❌ 50–100 service dumps per batch

---

## Definition of “long-running production-grade automation”

Only after:

1. Identity checks running on daily collect
2. Count-drift alerts observed across ≥2 weeks of upstream noise
3. BM-class path drift continues to surface via health + explicit registry fixes

Until then: **releasable for production routing of materialized sets**, with operational monitoring of Actions + `sources/health.yaml`.
