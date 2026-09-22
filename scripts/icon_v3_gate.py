#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re
import xml.etree.ElementTree as ET
from pathlib import Path
import yaml

STYLES = ("official","gradient","liquid_glass","soft_3d","minimal","dark_neon","monochrome")
CLIENTS = ("mihomo","singbox","surge","shadowrocket","quantumultx","egern","loon")

def valid_svg(path: Path) -> bool:
    try:
        root = ET.fromstring(path.read_text(encoding="utf-8"))
        return root.tag.rsplit("}",1)[-1] == "svg" and len(re.split(r"[\s,]+", root.attrib.get("viewBox","").strip())) == 4
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
    config = yaml.safe_load((Path(__file__).resolve().parents[1] / "config" / "icon_v3.yaml").read_text(encoding="utf-8")) or {}
    official_sites = yaml.safe_load((Path(__file__).resolve().parents[1] / "config" / "official_sites.yaml").read_text(encoding="utf-8")) or {}
    protected = {str(x).lower() for x in (config.get("protected_brands") or [])}
    errors = []
    if data.get("styles") != list(STYLES):
        errors.append("style contract mismatch")
    if data.get("clients") != list(CLIENTS):
        errors.append("client contract mismatch")
    for entry in data.get("entries", []):
        sid = entry.get("service_id")
        eligible = bool(entry.get("release_eligible", True))
        identity = entry.get("quality",{}).get("identity")
        expected_identity = "pass" if eligible or entry.get("role") != "service" else "hold"
        if identity != expected_identity:
            errors.append(f"{sid}: identity QA status={identity!r}, expected={expected_identity!r}")
        base = entry.get("base_asset",{})
        if not re.fullmatch(r"[0-9a-f]{64}", str(base.get("digest") or "")):
            errors.append(f"{sid}: invalid base digest")
        if eligible and entry.get("role") == "service":
            tier = str(base.get("source_tier") or "")
            license_meta = base.get("license") or {}
            license_type = str(license_meta.get("type") or "").lower()
            reviewed = license_meta.get("reviewed") is True
            if tier not in {"official", "trusted_third_party"}:
                errors.append(f"{sid}: stable service icon has unsupported source tier={tier}")
            if tier == "trusted_third_party" and not reviewed:
                errors.append(f"{sid}: stable third-party icon lacks reviewed license metadata")
            key = str(sid).lower()
            if key in protected and not (base.get("official_reference") or official_sites.get(str(sid)) or official_sites.get(str(sid).lower())):
                errors.append(f"{sid}: protected brand lacks official identity reference")
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

    try:
        state_path = Path(__file__).resolve().parents[1] / "config" / "source_canary_state.yaml"
        state = yaml.safe_load(state_path.read_text(encoding="utf-8")) or {}
        production_services = {
            sid for sid,row in (state.get("services") or {}).items()
            if isinstance(row,dict) and row.get("state")=="production" and row.get("enabled") is True
        }
        by_id = {e.get("service_id"): e for e in data.get("entries",[])}
        for sid in sorted(production_services):
            row = by_id.get(sid)
            if not row:
                errors.append(f"{sid}: production service has no Icon System 3 entry")
                continue
            if not row.get("release_eligible"):
                errors.append(f"{sid}: production service icon is quarantined")
            if row.get("role") != "service":
                errors.append(f"{sid}: production service icon role must be service")
    except Exception as exc:
        errors.append(f"production icon coverage check failed: {exc}")

    result = {"schema":"icon_v3_gate_v1","status":"PASS" if not errors else "FAIL","entry_count":len(data.get("entries",[])),"errors":errors}
    (root/"reports").mkdir(parents=True, exist_ok=True)
    (root/"reports"/"gate.json").write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["status"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
