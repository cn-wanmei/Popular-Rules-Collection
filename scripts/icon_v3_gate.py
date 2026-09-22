#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re
import xml.etree.ElementTree as ET
from pathlib import Path

STYLES = ("official","gradient","liquid_glass","soft_3d","minimal","dark_neon","monochrome")
CLIENTS = ("mihomo","singbox","surge","shadowrocket","quantumultx","egern","loon")

def valid_svg(path: Path) -> bool:
    try:
        root = ET.fromstring(path.read_text(encoding="utf-8"))
        return root.tag.rsplit("}",1)[-1] == "svg" and len(re.split(r"[\\s,]+", root.attrib.get("viewBox","").strip())) == 4
    except Exception:
        return False

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--build-root", type=Path, required=True)
    args = ap.parse_args()
    root = args.build_root
    manifest_path = root / "manifest.json"
    if not manifest_path.is_file():
        raise SystemExit("Icon System 3 Gate: manifest.json missing")
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    errors = []
    if data.get("styles") != list(STYLES):
        errors.append("style contract mismatch")
    if data.get("clients") != list(CLIENTS):
        errors.append("client contract mismatch")
    for entry in data.get("entries", []):
        sid = entry.get("service_id")
        if entry.get("quality",{}).get("identity") != "pass":
            errors.append(f"{sid}: identity QA failed")
        base = entry.get("base_asset",{})
        if not re.fullmatch(r"[0-9a-f]{64}", str(base.get("digest") or "")):
            errors.append(f"{sid}: invalid base digest")
        prov = entry.get("provenance",{})
        for field in ("source_provider","source_path","renderer_version","workspace_commit","generation_run_id"):
            if not str(prov.get(field) or "").strip():
                errors.append(f"{sid}: missing provenance {field}")
        for style in STYLES:
            row = (entry.get("variants") or {}).get(style) or {}
            path = root / str(row.get("path") or "")
            if not path.is_file():
                errors.append(f"{sid}:{style}: missing asset")
                continue
            if not valid_svg(path):
                errors.append(f"{sid}:{style}: invalid SVG")
            if row.get("digest") != hashlib.sha256(path.read_bytes()).hexdigest():
                errors.append(f"{sid}:{style}: digest mismatch")
    for style in STYLES:
        if not (root/"previews"/style/"master-all.svg").is_file():
            errors.append(f"missing master preview {style}")
        for size in (24,32,48):
            if not (root/"previews"/style/f"legibility-{size}.svg").is_file():
                errors.append(f"missing legibility {style}:{size}")
    if not (root/"icon-review-manifest.json").is_file():
        errors.append("missing icon-review-manifest.json")
    result = {"schema":"icon_v3_gate_v1","status":"PASS" if not errors else "FAIL","entry_count":len(data.get("entries",[])),"errors":errors}
    (root/"reports").mkdir(parents=True, exist_ok=True)
    (root/"reports"/"gate.json").write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["status"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
