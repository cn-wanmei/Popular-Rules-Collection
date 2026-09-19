#!/usr/bin/env python3
"""Phase E: compare two canonical roots by relative file path and SHA-256."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

ALLOWED = {".yaml", ".yml", ".json", ".jsonl", ".list", ".txt", ".mmdb"}

def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def inventory(root: Path) -> dict[str, str]:
    return {
        p.relative_to(root).as_posix(): digest(p)
        for p in root.rglob("*")
        if p.is_file() and p.suffix.lower() in ALLOWED
    }

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("left", type=Path)
    ap.add_argument("right", type=Path)
    args = ap.parse_args()
    errors: list[str] = []
    for label, root in (("left", args.left), ("right", args.right)):
        if not root.is_dir():
            errors.append(f"{label} root does not exist: {root}")

    left = inventory(args.left) if args.left.is_dir() else {}
    right = inventory(args.right) if args.right.is_dir() else {}
    missing_right = sorted(set(left) - set(right))
    extra_right = sorted(set(right) - set(left))
    changed = sorted(k for k in set(left) & set(right) if left[k] != right[k])
    if args.left.is_dir() and not left:
        errors.append(f"left root contains no supported rule files: {args.left}")
    if args.right.is_dir() and not right:
        errors.append(f"right root contains no supported rule files: {args.right}")
    payload = {
        "schema": "phase_e_dual_track_equivalence_v1",
        "left": str(args.left),
        "right": str(args.right),
        "left_files": len(left),
        "right_files": len(right),
        "missing_right": missing_right,
        "extra_right": extra_right,
        "changed": changed,
        "pass": not errors and not missing_right and not extra_right and not changed,
        "errors": errors,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["pass"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
