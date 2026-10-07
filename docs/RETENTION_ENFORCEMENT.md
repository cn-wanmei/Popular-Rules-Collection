# Retention enforcement (P2)

Policy SSOT: `config/retention.yaml` (backup keep_days=30, release evidence keep_days=180 per PUBLISH_STATUS).

## Current

- `scripts/retention.py` exists.
- Counts shown in `PUBLISH_STATUS.md` automated section.

## Hardening checklist

1. Scheduled workflow job weekly: `python scripts/retention.py --apply` (or dry-run + report artifact).
2. Fail or warn if `backup/` age exceeds policy without exception file.
3. Report repo size / largest paths in ecosystem-status.
4. Never delete `data/runs/<run>` still referenced by last N production pointers.

Status 2026-10-07: documentation only; wire schedule in follow-up PR after dry-run evidence.
