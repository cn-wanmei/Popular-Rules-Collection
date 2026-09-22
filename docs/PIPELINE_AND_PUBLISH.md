# Pipeline & Publish

## Current production entry points
```bash
python -m src.engine.cli all
python -m src.engine.cli naming_gate
python -m src.engine.cli promote --run-id <id>
python -m src.engine.cli rollback --run-id <id>
```

## Production flow
upstream → immutable backup → V3 Engine → Canonical → Semantic IR → 7 Client Adapters + Network Dataset → gates → Release Candidate → atomic publish → `generated/`.

## Truth boundary
- `data/runs/<run-id>/canonical/`：V3 Canonical
- `data/runs/<run-id>/ir/`：Semantic IR
- `generated/`：最终发行层
- `rule/`：V1 历史浏览/迁移树
- `rules/`：V3 目录契约
- `database/services/`：Legacy evidence

Legacy deletion is never automatic。