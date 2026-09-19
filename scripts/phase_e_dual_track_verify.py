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
    if not root.is_dir():
        return {}
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
    left = inventory(args.left)
    right = inventory(args.right)
    missing_right = sorted(set(left) - set(right))
    extra_right = sorted(set(right) - set(left))
    changed = sorted(k for k in set(left) & set(right) if left[k] != right[k])
    payload = {
        "schema": "phase_e_dual_track_equivalence_v1",
        "left": str(args.left),
        "right": str(args.right),
        "left_files": len(left),
        "right_files": len(right),
        "missing_right": missing_right,
        "extra_right": extra_right,
        "changed": changed,
        "pass": not missing_right and not extra_right and not changed,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["pass"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
