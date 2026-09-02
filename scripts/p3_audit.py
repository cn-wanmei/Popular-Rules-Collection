#!/usr/bin/env python3
"""P3 audit CLI: semantic diff, dependency lock, SBOM, checksums and release manifest."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from src.engine.audit.core import (
    build_provenance_graph,
    dependency_lock_report,
    generate_sbom,
    semantic_rule_diff,
    verify_action_shas,
    write_checksum_manifest,
    write_release_manifest,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["diff", "lock", "sbom", "checksums", "actions", "manifest"])
    parser.add_argument("--current", type=Path, default=Path("generated/canonical/rules.jsonl"))
    parser.add_argument("--baseline", type=Path, default=Path("reports/diff/baseline.jsonl"))
    parser.add_argument("--artifacts", type=Path, default=Path("generated"))
    parser.add_argument("--out", type=Path, default=Path("reports/audit"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    if args.command == "diff":
        result = semantic_rule_diff(args.current, args.baseline if args.baseline.exists() else None)
        target = args.out / "semantic_diff.json"
    elif args.command == "lock":
        result = dependency_lock_report(Path("requirements.lock"))
        target = args.out / "dependency_lock.json"
    elif args.command == "sbom":
        result = generate_sbom(Path("requirements.lock"), args.out / "sbom.cdx.json")
        target = args.out / "sbom.cdx.json"
    elif args.command == "checksums":
        result = write_checksum_manifest(args.artifacts, args.out / "artifact_checksums.json")
        target = args.out / "artifact_checksums.json"
    elif args.command == "actions":
        result = verify_action_shas(Path(".github/workflows"))
        target = args.out / "action_sha_verification.json"
    else:
        sbom = args.out / "sbom.cdx.json"
        checksums = args.out / "artifact_checksums.json"
        if not sbom.exists():
            generate_sbom(Path("requirements.lock"), sbom)
        if not checksums.exists():
            write_checksum_manifest(args.artifacts, checksums)
        diff = semantic_rule_diff(args.current, args.baseline if args.baseline.exists() else None)
        provenance = build_provenance_graph([])
        version = Path("VERSION").read_text(encoding="utf-8").strip() if Path("VERSION").exists() else "unknown"
        result = write_release_manifest(args.out / "release_manifest.json", version=version,
                                        commit=os.getenv("GITHUB_SHA", "workspace"), artifacts=args.artifacts,
                                        sbom=sbom, checksums=checksums, semantic_diff=diff,
                                        provenance=provenance)
        target = args.out / "release_manifest.json"

    target.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8") if target != args.out / "sbom.cdx.json" and target != args.out / "artifact_checksums.json" and target != args.out / "release_manifest.json" else None
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("pass", result.get("locked", True)) else 1


if __name__ == "__main__":
    raise SystemExit(main())
