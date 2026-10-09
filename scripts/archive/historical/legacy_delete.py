"""Manual operator entrypoint for Phase 8 Legacy deletion."""
from __future__ import annotations
import argparse
import subprocess
from pathlib import Path
from src.engine.legacy.delete import delete_legacy
ROOT = Path(__file__).resolve().parents[1]
def main() -> int:
    parser = argparse.ArgumentParser(description="Explicitly delete database/services after final V1 migration gate")
    parser.add_argument("--gate", type=Path, default=ROOT / "reports/v1/FINAL_MIGRATION_GATE.json")
    parser.add_argument("--approve", action="store_true", help="explicit operator approval")
    args = parser.parse_args()
    current_head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    result = delete_legacy(
        args.gate,
        Path("database/services"),
        explicit_approval=args.approve,
        current_head=current_head,
    )
    print(result)
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
