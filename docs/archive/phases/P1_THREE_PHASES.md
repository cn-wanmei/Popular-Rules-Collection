# P1 Three Phases

## Phase 1 — Semantic tools
- `build_universal_ir.py` → `generated/ir/`
- `semantic_dedup.py` / `growth_anomaly.py`
- `config/ci_gates.yaml`

## Phase 2 — Provenance
- `attach_artifact_provenance.py` → `generated/_meta/provenance.json`

## Phase 3 — Cross-client sample
- `cross_client_semantic_test.py` (openai/github/telegram/apple/google)

See also `docs/P2_ADVANCE_ANALYSIS.md`.
