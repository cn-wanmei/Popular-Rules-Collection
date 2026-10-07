# Retention enforcement

SSOT: `config/retention.yaml`  
Script: `scripts/retention.py` (default dry-run; `--apply` destructive)

## Workflow (on main)

`.github/workflows/retention.yml`:

| Trigger | Behavior |
|---------|----------|
| `schedule` weekly Mon 06:00 UTC | **dry-run only** + upload `retention_plan.txt` |
| `workflow_dispatch` + `apply=false` | dry-run |
| `workflow_dispatch` + `apply=true` | destructive `--apply` |

Respects `keep_min_successful` on `backup/` and `data/runs/`.
