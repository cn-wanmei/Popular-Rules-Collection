"""HARD gate: forbid product/path namespaces named v3 (codename-only allowed)."""
from __future__ import annotations
from pathlib import Path

def check_repo_layout(root: Path) -> list[str]:
    errors: list[str] = []
    for rel in ("src/v3", "data/v3", "config/v3", "tests/v3", "reports/v3", "generated/v3"):
        if (root / rel).exists():
            errors.append(f"forbidden path exists: {rel}")
    if (root / "src" / "v3").is_dir():
        errors.append("Python package src.v3 must not exist; use src.engine")
    return errors

def main() -> int:
    root = Path(__file__).resolve().parents[3]
    errs = check_repo_layout(root)
    print(f"[naming_gate] errors={len(errs)}")
    for e in errs:
        print(f"  ERROR {e}")
    return 1 if errs else 0

if __name__ == "__main__":
    raise SystemExit(main())
