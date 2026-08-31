# P2 Advance Analysis

## Ready?
P0 semantic fixes + P1 IR/provenance/sample differential are in. **Not** ready for full builder IR migration or `src/` rewrite.

## P2 order
1. **Release artifact split** — large lists/MMDB out of Git
2. **Source trust + quarantine** — use growth_anomaly
3. **HARD/SOFT enforcement** from `ci_gates.yaml`
4. **One-client IR pilot** (Mihomo) + golden tests
5. **Directory layout** last

## Avoid
- Mass new sources
- Deleting service subscriptions
- All-client IR flip without golden corpus
