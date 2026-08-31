#!/usr/bin/env python3
"""V2.3 Run gated step: shadow logs would_block; enforce fails job."""
from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
GATES = ROOT / "config" / "ci_gates.yaml"
LOG = ROOT / "reports" / "gate_runs.jsonl"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("cmd", nargs=argparse.REMAINDER)
    args = ap.parse_args()
    if args.cmd and args.cmd[0] == "--":
        args.cmd = args.cmd[1:]
    doc = yaml.safe_load(GATES.read_text(encoding="utf-8")) if GATES.exists() else {}
    mode = doc.get("mode") or "shadow"
    action = (doc.get("gates") or {}).get(args.name) or "WARN"
    if not args.cmd:
        print(f"[run_gated] {args.name} action={action} mode={mode}")
        return 0
    r = subprocess.run(args.cmd, cwd=ROOT)
    code = r.returncode
    would_block = code != 0 and action in ("BLOCK_BUILD", "BLOCK_RELEASE")
    rec = {"ts": datetime.now(timezone.utc).isoformat(), "name": args.name, "action": action, "mode": mode, "exit": code, "would_block": would_block, "enforced": mode == "enforce" and would_block}
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")
    print(f"[run_gated] {args.name} exit={code} action={action} mode={mode} would_block={would_block}")
    if mode == "enforce" and would_block:
        return code if code else 1
    return 0 if mode == "shadow" else code


if __name__ == "__main__":
    raise SystemExit(main())
