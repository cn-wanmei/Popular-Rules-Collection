#!/usr/bin/env python3
"""Validate Path Links G3 READMEs under rule/ and generated/."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML required", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
CLIENTS = ["egern", "loon", "mihomo", "quantumultx", "shadowrocket", "singbox", "surge"]
START = "<!-- PATH_LINKS_GENERATED_START -->"
RAW_RE = re.compile(
    r"generated/((?:egern|loon|mihomo|quantumultx|shadowrocket|singbox|surge)/[A-Za-z0-9_.\-/]+\.(?:yaml|json|list))"
)


def main() -> int:
    errors: list[str] = []
    idx = yaml.safe_load((ROOT / "rule" / "_index.yaml").read_text(encoding="utf-8")) or {}
    man = json.loads((ROOT / "generated" / "manifest.json").read_text(encoding="utf-8"))
    man_files = {
        f["file"] for f in man.get("files") or [] if f.get("kind") == "client_rules" and f.get("file")
    }
    entries = idx.get("entries") or []

    for ent in entries:
        sid = str(ent["id"])
        path = ent["path"]
        readme = ROOT / "rule" / Path(path).parent / "README.md"
        if not readme.is_file():
            errors.append(f"missing rule path link: {readme.relative_to(ROOT)}")
            continue
        text = readme.read_text(encoding="utf-8")
        if START not in text:
            errors.append(f"{readme.relative_to(ROOT)}: missing PATH_LINKS marker")
        if f"docs/rules/{sid}.md" not in text:
            errors.append(f"{readme.relative_to(ROOT)}: missing docs link for {sid}")
        for m in RAW_RE.findall(text):
            if m not in man_files:
                errors.append(f"{readme.relative_to(ROOT)}: non-manifest path {m}")

    # Sample generated leaves: every manifest client_rules dir should have README
    missing_gen = 0
    for rel in sorted(man_files):
        readme = ROOT / "generated" / Path(rel).parent / "README.md"
        if not readme.is_file():
            missing_gen += 1
            if missing_gen <= 25:
                errors.append(f"missing generated path link: {readme.relative_to(ROOT)}")
    if missing_gen > 25:
        errors.append(f"missing generated path link: ... {missing_gen - 25} more")

    for root_readme in (ROOT / "rule" / "README.md", ROOT / "generated" / "README.md"):
        if not root_readme.is_file():
            errors.append(f"missing {root_readme.relative_to(ROOT)}")

    if errors:
        print("validate_path_links: FAIL")
        for e in errors[:80]:
            print(" ", e)
        if len(errors) > 80:
            print(f"  ... +{len(errors) - 80} more")
        return 1
    print(
        f"validate_path_links: OK (rule_entries={len(entries)} client_files={len(man_files)})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
