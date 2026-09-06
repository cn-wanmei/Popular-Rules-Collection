#!/usr/bin/env python3
"""Deterministic repository-wide Icon QA."""
from __future__ import annotations

import argparse
import json
import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ICON_ROOT = ROOT / "assets/icons"
MANIFEST = ICON_ROOT / "manifest.yaml"
SIZES = (64, 128, 256)
PAYMENT_KEYS = {
    "applepay": {"apple pay", "applepay", "apple-pay", "apple_pay", "apay"},
    "googlepay": {"google pay", "googlepay", "google-pay", "google_pay", "gpay"},
    "unionpay": {"unionpay", "union pay", "union-pay", "union_pay", "银联"},
}
FORBIDDEN = {
    "applepay": {"apple"},
    "googlepay": {"google"},
    "unionpay": {"visa", "mastercard", "alipay", "wechatpay", "wechat"},
}
STOPWORDS = {"icon", "logo", "brand", "service", "official", "app", "the"}


def norm(s):
    return re.sub(r"[^a-z0-9]+", "", str(s).lower())


def tokens(s):
    return {
        x
        for x in re.findall(r"[a-z0-9]+", str(s).lower())
        if x not in STOPWORDS and len(x) > 1
    }


def image_size(path):
    from PIL import Image

    with Image.open(path) as im:
        im.verify()
    with Image.open(path) as im:
        return im.size, im.mode, im.getbbox()


def svg_meta(path):
    text = path.read_text(encoding="utf-8")
    root = ET.fromstring(text)
    vb = root.attrib.get("viewBox", "")
    nums = [float(x) for x in re.split(r"[\s,]+", vb.strip()) if x] if vb else []
    aspect = nums[2] / nums[3] if len(nums) == 4 and nums[2] > 0 and nums[3] > 0 else None
    title = ""
    for c in root.iter():
        if c.tag.rsplit("}", 1)[-1] == "title" and c.text:
            title = c.text.strip()
            break
    return {
        "bytes": path.stat().st_size,
        "viewBox": vb,
        "aspect": aspect,
        "title": title,
        "root": root.tag.rsplit("}", 1)[-1],
    }


def semantic_match(key: str, name: str, title: str, aliases: set[str]) -> bool:
    if not title:
        return True
    nk, nn, nt = norm(key), norm(name), norm(title)
    if key in PAYMENT_KEYS:
        return nt == norm(name) or nt in {norm(x) for x in PAYMENT_KEYS[key]}
    if nt in {nk, nn} or nt in aliases or nk in nt or nn in nt:
        return True
    title_tokens = tokens(title)
    candidate_tokens = tokens(name) | tokens(key)
    for alias in aliases:
        candidate_tokens |= tokens(alias)
    return bool(title_tokens & candidate_tokens)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default="reports/icon_qa.json")
    args = ap.parse_args()
    doc = yaml.safe_load(MANIFEST.read_text(encoding="utf-8")) or {}
    icons = doc.get("icons") or {}
    report = {
        "schema": "icon_qa_v3",
        "icon_count": len(icons),
        "checks": {
            "source_svg": 0,
            "png_64": 0,
            "png_128": 0,
            "png_256": 0,
            "semantic": 0,
            "payment_separation": 0,
            "payment_provenance": 0,
        },
        "errors": [],
        "warnings": [],
    }

    for key, meta in sorted(icons.items()):
        if not isinstance(meta, dict):
            report["errors"].append(f"{key}: manifest entry is not a mapping")
            continue
        files = meta.get("files") or {}
        svg_rel = files.get("svg") or f"source/{key}.svg"
        svg = ICON_ROOT / svg_rel
        if not svg.is_file():
            report["errors"].append(f"{key}: missing SVG {svg_rel}")
            continue
        try:
            sm = svg_meta(svg)
            report["checks"]["source_svg"] += 1
            if sm["root"] != "svg":
                report["errors"].append(f"{key}: source root is not <svg>")
            if not sm["viewBox"] or sm["aspect"] is None or not math.isfinite(sm["aspect"]):
                report["errors"].append(f"{key}: invalid or missing SVG viewBox")
        except Exception as exc:
            report["errors"].append(f"{key}: invalid SVG: {exc}")
            continue

        for size in SIZES:
            rel = (files.get("png") or {}).get(str(size)) or f"png/{size}/{key}.png"
            p = ICON_ROOT / rel
            if not p.is_file():
                report["errors"].append(f"{key}: missing PNG {size} {rel}")
                continue
            try:
                wh, mode, bbox = image_size(p)
                report["checks"][f"png_{size}"] += 1
            except Exception as exc:
                report["errors"].append(f"{key}: unreadable PNG {rel}: {exc}")
                continue
            if wh != (size, size):
                report["errors"].append(f"{key}: PNG {size} is {wh[0]}x{wh[1]}, expected {size}x{size}")
            if mode not in {"RGB", "RGBA"}:
                report["errors"].append(f"{key}: PNG {size} has unsupported mode {mode}")
            if bbox is None:
                report["errors"].append(f"{key}: PNG {size} is completely blank")

        name = str(meta.get("name") or key)
        title = sm.get("title", "")
        aliases = {str(x) for x in (meta.get("aliases") or []) if x}
        if semantic_match(key, name, title, aliases):
            report["checks"]["semantic"] += 1
        else:
            report["errors"].append(f"{key}: semantic mismatch name={name!r} svg_title={title!r}")

        if key in PAYMENT_KEYS:
            report["checks"]["payment_separation"] += 1
            slug = norm((meta.get("source") or {}).get("slug") or "")
            if slug in {norm(x) for x in FORBIDDEN[key]}:
                report["errors"].append(f"{key}: forbidden generic brand fallback {slug}")
            source = meta.get("source") or {}
            if source.get("provider") != "datatrans/payment-logos":
                report["errors"].append(f"{key}: unexpected payment source provider {source.get('provider')!r}")
            if source.get("license") != "CC-BY-SA-4.0":
                report["errors"].append(f"{key}: missing/incorrect payment source license metadata")
            report["checks"]["payment_provenance"] += 1

        status = str(meta.get("status") or "")
        if status in {"missing", "placeholder", "review"}:
            report["warnings"].append(f"{key}: manifest status={status}")

    out = ROOT / args.json
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = {
        "icons": report["icon_count"],
        "errors": len(report["errors"]),
        "warnings": len(report["warnings"]),
        "checks": report["checks"],
        "report": str(out),
    }
    print(json.dumps(summary, ensure_ascii=False))
    if report["errors"]:
        print("[icon_qa] errors:")
        for error in report["errors"]:
            print(f" - {error}")
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
