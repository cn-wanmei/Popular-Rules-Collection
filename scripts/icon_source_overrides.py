#!/usr/bin/env python3
"""Apply protected semantic sources for payment brands after generic refresh."""
from __future__ import annotations

from pathlib import Path
import urllib.request
import xml.etree.ElementTree as ET

import yaml

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets/icons/source"
MAN = ROOT / "assets/icons/manifest.yaml"
UA = {"User-Agent": "PRC-Icons/2.0"}
URLS = {
    "applepay": "https://raw.githubusercontent.com/datatrans/payment-logos/master/assets/wallets/apple-pay.svg",
    "googlepay": "https://raw.githubusercontent.com/datatrans/payment-logos/master/assets/wallets/google-pay.svg",
    "unionpay": "https://raw.githubusercontent.com/datatrans/payment-logos/master/assets/cards/unionpay.svg",
}
TITLES = {"applepay": "Apple Pay", "googlepay": "Google Pay", "unionpay": "UnionPay"}


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as response:
        return response.read().decode("utf-8")


def validate_svg(key: str, text: str) -> None:
    try:
        root = ET.fromstring(text)
    except ET.ParseError as exc:
        raise SystemExit(f"{key}: downloaded payment source is invalid SVG: {exc}") from exc
    if root.tag.rsplit("}", 1)[-1] != "svg":
        raise SystemExit(f"{key}: downloaded payment source root is not <svg>")
    if len(root.attrib.get("viewBox", "").split()) != 4:
        raise SystemExit(f"{key}: downloaded payment source has no valid viewBox")
    titles = {
        (node.text or "").strip()
        for node in root.iter()
        if node.tag.rsplit("}", 1)[-1] == "title"
    }
    if TITLES[key] not in titles:
        raise SystemExit(f"{key}: downloaded payment source title mismatch: {sorted(titles)!r}")


def wrap(key: str, inner: str) -> str:
    inner = inner.replace(
        '<svg',
        '<g transform="translate(4 24)"',
        1,
    ).replace('</svg>', '</g>', 1)
    title = TITLES[key]
    return (
        '<svg role="img" viewBox="0 0 128 128" xmlns="http://www.w3.org/2000/svg">'
        f'<title>{title}</title>'
        '<rect width="128" height="128" rx="28" fill="#F7F7F7"/>'
        f"{inner}</svg>"
    )


def update_manifest() -> None:
    doc = yaml.safe_load(MAN.read_text(encoding="utf-8")) or {}
    icons = doc.setdefault("icons", {})
    for key, url in URLS.items():
        meta = icons.setdefault(key, {})
        meta.setdefault("name", TITLES[key])
        meta.setdefault("type", "service")
        meta.setdefault("icon_key", key)
        source = meta.setdefault("source", {})
        source.update(
            {
                "provider": "datatrans/payment-logos",
                "type": "payment-logo",
                "provenance": "third_party",
                "verified": True,
                "url": url,
                "license": "CC-BY-SA-4.0",
            }
        )
        files = meta.setdefault("files", {})
        files["svg"] = f"source/{key}.svg"
        files.setdefault("png", {})
        meta["license"] = {
            "type": "CC-BY-SA-4.0",
            "note": "Datatrans payment-logos asset; attribution/share-alike terms apply.",
            "reviewed": True,
        }
        icons[key] = meta
    doc["icons"] = icons
    MAN.write_text(yaml.dump(doc, allow_unicode=True, sort_keys=False, width=100), encoding="utf-8")


def main() -> None:
    SRC.mkdir(parents=True, exist_ok=True)
    for key, url in URLS.items():
        raw = fetch(url)
        validate_svg(key, raw)
        (SRC / f"{key}.svg").write_text(wrap(key, raw), encoding="utf-8")
    update_manifest()
    print("[icon_payment_overrides] updated=3, manifest=3")


if __name__ == "__main__":
    main()
