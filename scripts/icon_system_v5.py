#!/usr/bin/env python3
"""Icon System V5: source acquisition, eight-layer rendering, registry and gates."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

import yaml

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "config" / "icon_v5.yaml"
OFFICIAL_SITES = ROOT / "config" / "official_sites.yaml"
VARIANTS = (
    "source_original",
    "glassmorphism",
    "soft_3d",
    "neo_skeuomorphism",
    "minimalist",
    "duotone_line",
    "mbe",
    "y2k",
)
STYLE_VARIANTS = VARIANTS[1:]
RENDERER_VERSION = "prc-icon-renderer-v5.0.0"


def sha256(data: bytes | str) -> str:
    raw = data.encode("utf-8") if isinstance(data, str) else data
    return hashlib.sha256(raw).hexdigest()


def load_yaml(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return value if isinstance(value, dict) else {}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def slug(value: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9._-]+", "-", str(value).strip().lower())
    return text.strip("-._") or "unknown"


def discover_services(rule_index: Path) -> list[dict]:
    doc = load_yaml(rule_index)
    rows = []
    seen = set()
    for row in doc.get("entries") or []:
        if not isinstance(row, dict) or row.get("entity") != "service":
            continue
        sid = str(row.get("id") or "").strip()
        if not sid:
            continue
        if sid in seen:
            raise ValueError(f"duplicate service_id in rule index: {sid}")
        seen.add(sid)
        rows.append({
            "service_id": sid,
            "display_name": str(row.get("display_name") or sid),
            "provider": row.get("provider"),
            "rule_path": str(row.get("path") or ""),
            "rule_count": int(row.get("rule_count") or 0),
        })
    if not rows:
        raise ValueError("no service entities discovered")
    return sorted(rows, key=lambda x: x["service_id"])


def candidate_domains(root: Path, row: dict) -> list[str]:
    path = root / row["rule_path"]
    if not path.is_file():
        return []
    try:
        doc = load_yaml(path)
    except Exception:
        return []
    values = []
    for rule in doc.get("rules") or []:
        if not isinstance(rule, dict):
            continue
        kind = str(rule.get("type") or "").upper()
        value = str(rule.get("value") or "").strip()
        if value and kind in {"DOMAIN", "DOMAIN_SUFFIX", "DOMAIN_KEYWORD"}:
            values.append(value.lstrip("."))
    hosts = []
    for value in values:
        host = value
        if "://" in host:
            host = urlparse(host).hostname or ""
        host = host.split("/")[0].strip().lower().rstrip(".")
        if not re.fullmatch(r"[a-z0-9.-]+\.[a-z]{2,}", host):
            continue
        if any(bad in host for bad in (
            "cdn.", "static.", "img.", "image.", "images.", "assets.",
            "download.", "update.", "api.", "gateway.", "cloudfront.net",
            "akamaized.net", "fastly.net", "githubusercontent.com",
        )):
            continue
        if host not in hosts:
            hosts.append(host)
    tokens = re.findall(r"[a-z0-9]+", str(row["service_id"]).lower())
    display_tokens = re.findall(r"[a-z0-9]+", str(row["display_name"]).lower())
    return sorted(
        hosts,
        key=lambda h: (
            -sum(1 for t in tokens + display_tokens if t and t in h),
            h.count("."),
            h,
        ),
    )[:8]


def official_url(sid: str, official: dict) -> str | None:
    value = official.get(sid)
    return str(value).strip() if value else None


class IconLinkParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []

    def handle_starttag(self, tag, attrs):
        data = {str(k).lower(): str(v or "") for k, v in attrs}
        if tag.lower() != "link":
            return
        rel = {x.strip().lower() for x in data.get("rel", "").split()}
        href = data.get("href", "").strip()
        if href and rel & {"icon", "shortcut", "apple-touch-icon", "apple-touch-icon-precomposed"}:
            self.links.append((" ".join(sorted(rel)), href))


def fetch_bytes(url: str, *, timeout: int, max_bytes: int, user_agent: str) -> tuple[bytes, dict]:
    parsed = urlparse(url)
    if parsed.scheme.lower() != "https":
        raise ValueError(f"only https is allowed: {url}")
    req = Request(url, headers={"User-Agent": user_agent, "Accept": "*/*"})
    with urlopen(req, timeout=timeout) as response:
        final_url = response.geturl()
        if urlparse(final_url).scheme.lower() != "https":
            raise ValueError(f"redirected to non-https: {final_url}")
        content = response.read(max_bytes + 1)
        if len(content) > max_bytes:
            raise ValueError(f"response exceeds {max_bytes} bytes")
        return content, {
            "status_code": getattr(response, "status", None),
            "content_type": response.headers.get("Content-Type"),
            "final_url": final_url,
        }


def validate_source(content: bytes, content_type: str | None, source_url: str) -> str:
    ctype = (content_type or "").split(";", 1)[0].strip().lower()
    if content.lstrip().lower().startswith(b"<svg"):
        kind = "svg"
    elif content.startswith(b"\x89PNG\r\n\x1a\n"):
        kind = "png"
    elif len(content) >= 12 and content[:4] == b"RIFF" and content[8:12] == b"WEBP":
        kind = "webp"
    elif content.startswith(b"\x00\x00\x01\x00"):
        kind = "ico"
    else:
        allowed = {
            "image/svg+xml": "svg",
            "image/png": "png",
            "image/webp": "webp",
            "image/x-icon": "ico",
            "image/vnd.microsoft.icon": "ico",
            "image/jpeg": "jpg",
        }
        if ctype not in allowed:
            raise ValueError(f"unsupported icon content: {source_url} ({ctype or 'unknown'})")
        kind = allowed[ctype]
    if kind == "svg":
        try:
            root = ET.fromstring(content.decode("utf-8"))
        except Exception as exc:
            raise ValueError(f"invalid svg: {source_url}: {exc}") from exc
        forbidden = {"script", "foreignObject", "iframe", "object", "embed"}
        for node in root.iter():
            local = node.tag.rsplit("}", 1)[-1]
            if local in forbidden:
                raise ValueError(f"unsafe svg element {local}: {source_url}")
            for attr, value in node.attrib.items():
                if attr.rsplit("}", 1)[-1] in {"href", "src"}:
                    val = str(value).strip()
                    if val and not val.startswith("data:") and not val.startswith("#"):
                        raise ValueError(f"external svg reference: {source_url}")
    return kind


def svg_data_url(content: bytes, kind: str) -> str:
    mime = {
        "svg": "image/svg+xml",
        "png": "image/png",
        "webp": "image/webp",
        "ico": "image/x-icon",
        "jpg": "image/jpeg",
    }[kind]
    return "data:" + mime + ";base64," + base64.b64encode(content).decode("ascii")


def _xml_escape(value: str) -> str:
    return str(value).replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


def _svg_shell(body: str, title: str, background: str = "#ffffff") -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" role="img" aria-label="{_xml_escape(title)}">
  <defs>
    <filter id="shadow" x="-40%" y="-40%" width="180%" height="180%"><feDropShadow dx="0" dy="22" stdDeviation="22" flood-opacity=".20"/></filter>
    <filter id="soft" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="18"/></filter>
    <linearGradient id="cyber" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#00F0FF"/><stop offset=".5" stop-color="#7C4DFF"/><stop offset="1" stop-color="#FF2BD6"/></linearGradient>
  </defs>
  <rect width="512" height="512" rx="112" fill="{background}"/>
  {body}
</svg>'''


def render_variant(image_href: str, title: str, style: str) -> str:
    if style == "glassmorphism":
        body = f'''
  <circle cx="140" cy="130" r="140" fill="#8EC5FF" opacity=".34" filter="url(#soft)"/>
  <circle cx="388" cy="376" r="150" fill="#D79CFF" opacity=".30" filter="url(#soft)"/>
  <rect x="54" y="54" width="404" height="404" rx="96" fill="#FFFFFF" fill-opacity=".36" stroke="#FFFFFF" stroke-opacity=".72" stroke-width="4" filter="url(#shadow)"/>
  <rect x="66" y="66" width="380" height="380" rx="84" fill="none" stroke="#FFFFFF" stroke-opacity=".30" stroke-width="2"/>
  <image href="{image_href}" x="112" y="112" width="288" height="288" preserveAspectRatio="xMidYMid meet"/>
'''
    elif style == "soft_3d":
        body = f'''
  <rect x="60" y="76" width="392" height="392" rx="112" fill="#DDE7F6" filter="url(#shadow)"/>
  <rect x="48" y="48" width="392" height="392" rx="112" fill="#F8FAFC"/>
  <path d="M84 84h320" stroke="#FFFFFF" stroke-width="12" stroke-linecap="round" opacity=".9"/>
  <image href="{image_href}" x="118" y="128" width="276" height="276" preserveAspectRatio="xMidYMid meet" opacity=".28" transform="translate(8 14)"/>
  <image href="{image_href}" x="112" y="112" width="276" height="276" preserveAspectRatio="xMidYMid meet"/>
'''
    elif style == "neo_skeuomorphism":
        body = f'''
  <rect x="54" y="54" width="404" height="404" rx="92" fill="#E9EEF7" stroke="#FFFFFF" stroke-width="8" filter="url(#shadow)"/>
  <path d="M106 122c0-18 14-32 32-32h236" fill="none" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round" opacity=".9"/>
  <path d="M100 382c0 22 18 40 40 40h232" fill="none" stroke="#B7C2D6" stroke-width="12" stroke-linecap="round" opacity=".58"/>
  <rect x="88" y="88" width="336" height="336" rx="82" fill="none" stroke="#B7C2D6" stroke-width="4"/>
  <image href="{image_href}" x="122" y="122" width="268" height="268" preserveAspectRatio="xMidYMid meet"/>
'''
    elif style == "minimalist":
        body = f'''
  <circle cx="256" cy="256" r="196" fill="#F8FAFC"/>
  <path d="M126 382c42 34 84 50 130 50s88-16 130-50" fill="none" stroke="#CBD5E1" stroke-width="10" stroke-linecap="round"/>
  <circle cx="256" cy="256" r="164" fill="none" stroke="#E2E8F0" stroke-width="4"/>
  <image href="{image_href}" x="124" y="124" width="264" height="264" preserveAspectRatio="xMidYMid meet"/>
'''
    elif style == "duotone_line":
        body = f'''
  <rect x="48" y="48" width="416" height="416" rx="84" fill="#FFFFFF"/>
  <path d="M126 372V140h260v232z" fill="none" stroke="#111827" stroke-width="12" stroke-linejoin="round"/>
  <path d="M100 206h72M340 206h72M206 100v72M206 340v72" stroke="#7C3AED" stroke-width="12" stroke-linecap="round"/>
  <image href="{image_href}" x="132" y="132" width="248" height="248" preserveAspectRatio="xMidYMid meet" opacity=".92"/>
'''
    elif style == "mbe":
        body = f'''
  <path d="M82 176c-10-72 48-124 112-106 42-48 130-18 138 42 72 4 116 86 72 144 22 76-52 138-122 108-50 48-142 28-160-34-76 2-116-72-62-128z" fill="#F1F5FF" stroke="#111827" stroke-width="12" stroke-linejoin="round"/>
  <circle cx="108" cy="138" r="10" fill="#7C3AED"/>
  <circle cx="398" cy="148" r="10" fill="#06B6D4"/>
  <circle cx="410" cy="366" r="10" fill="#EC4899"/>
  <path d="M116 394l-34 38M394 388l38 36M410 108l30-24M100 106l-34-26" stroke="#111827" stroke-width="10" stroke-linecap="round"/>
  <image href="{image_href}" x="132" y="132" width="248" height="248" preserveAspectRatio="xMidYMid meet"/>
'''
    elif style == "y2k":
        body = f'''
  <rect x="40" y="40" width="432" height="432" rx="112" fill="#0B1020" stroke="#5BE7FF" stroke-width="6" filter="url(#shadow)"/>
  <rect x="58" y="58" width="396" height="396" rx="96" fill="none" stroke="url(#cyber)" stroke-width="10"/>
  <path d="M92 120h328M92 184h328M92 328h328M92 392h328" stroke="#FFFFFF" stroke-opacity=".08" stroke-width="2"/>
  <circle cx="394" cy="118" r="18" fill="#00F0FF" opacity=".85"/>
  <path d="M112 112l18 18M130 112l-18 18M382 380l22 22M404 380l-22 22" stroke="#FF2BD6" stroke-width="7" stroke-linecap="round"/>
  <image href="{image_href}" x="124" y="124" width="264" height="264" preserveAspectRatio="xMidYMid meet"/>
'''
    else:
        raise ValueError(f"unsupported style: {style}")
    return _svg_shell(body, title)


def write_preview(style: str, entries: list[dict], root: Path) -> None:
    cols = 8
    rows = (len(entries) + cols - 1) // cols
    width, height = cols * 104, rows * 120
    out = root / "previews" / style
    out.mkdir(parents=True, exist_ok=True)
    nodes = []
    for i, row in enumerate(entries):
        c, r = i % cols, i // cols
        x, y = c * 104 + 4, r * 120 + 4
        nodes.append(
            f'<rect x="{x}" y="{y}" width="96" height="96" rx="20" fill="#fff" stroke="#E2E8F0"/>'
            f'<image href="../styles/{style}/{slug(row["service_id"])}.svg" x="{x+8}" y="{y+8}" width="80" height="80"/>'
        )
    (out / "master-all.svg").write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">' + "".join(nodes) + "</svg>",
        encoding="utf-8",
    )


def resolve_source(root: Path, row: dict, official: dict, policy: dict) -> dict:
    sid = row["service_id"]
    homepage = official_url(sid, official)
    reason = "registered_official" if homepage else None
    if not homepage:
        candidates = candidate_domains(root, row)
        if candidates:
            homepage = "https://" + candidates[0] + "/"
            reason = "rule_domain_candidate"
    if not homepage:
        return {"status": "hold", "service_id": sid, "reason": "no_official_homepage_candidate"}
    acq = policy["acquisition"]
    page, page_headers = fetch_bytes(
        homepage,
        timeout=int(acq["timeout_seconds"]),
        max_bytes=int(acq["max_bytes"]),
        user_agent=str(acq["user_agent"]),
    )
    parser = IconLinkParser()
    parser.feed(page.decode("utf-8", errors="ignore"))
    icon_url = urljoin(page_headers["final_url"], parser.links[0][1]) if parser.links else urljoin(page_headers["final_url"], "/favicon.ico")
    icon, headers = fetch_bytes(
        icon_url,
        timeout=int(acq["timeout_seconds"]),
        max_bytes=int(acq["max_bytes"]),
        user_agent=str(acq["user_agent"]),
    )
    kind = validate_source(icon, headers.get("content_type"), headers["final_url"])
    return {
        "status": "ok",
        "service_id": sid,
        "homepage_url": page_headers["final_url"],
        "source_url": headers["final_url"],
        "source_kind": kind,
        "content_type": headers.get("content_type"),
        "source_digest": sha256(icon),
        "content": icon,
        "resolution_reason": reason,
        "homepage_digest": sha256(page),
    }


def build(args: argparse.Namespace) -> int:
    policy = load_yaml(POLICY)
    official = load_yaml(OFFICIAL_SITES)
    rule_index = Path(args.rule_index)
    entries = discover_services(rule_index)
    rule_doc = load_yaml(rule_index)
    lineage = {
        "run_id": str(args.run_id or rule_doc.get("run_id") or ""),
        "snapshot_id": str(args.snapshot_id or ""),
        "ir_digest": str(args.ir_digest or rule_doc.get("ir_digest") or ""),
    }
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "source" / "original").mkdir(parents=True, exist_ok=True)
    (out / "normalized").mkdir(parents=True, exist_ok=True)
    for style in STYLE_VARIANTS:
        (out / "styles" / style).mkdir(parents=True, exist_ok=True)

    results = []
    acquired_by_url: dict[str, dict] = {}
    for row in entries:
        try:
            result = resolve_source(ROOT, row, official, policy)
        except Exception as exc:
            result = {"status": "hold", "service_id": row["service_id"], "reason": f"{type(exc).__name__}: {exc}"}
        if result.get("status") != "ok":
            results.append({
                **row,
                "icon_identity": f"service:{row['service_id']}",
                "source": {
                    "origin": "unresolved",
                    "homepage_url": result.get("homepage_url"),
                    "source_url": result.get("source_url"),
                    "digest": None,
                    "rights_basis": "review",
                    "redistribution_status": "review",
                    "reason": result.get("reason"),
                },
                "variants": {},
                "lineage": {**lineage, "source_digest": None, "renderer_version": RENDERER_VERSION},
                "release_eligible": False,
            })
            continue

        source_url = str(result["source_url"])
        if source_url in acquired_by_url:
            cached = acquired_by_url[source_url]
            result = {**result, "content": cached["content"], "source_digest": cached["source_digest"], "source_kind": cached["source_kind"]}
        else:
            acquired_by_url[source_url] = result

        kind = result["source_kind"]
        ext = {"svg": "svg", "png": "png", "webp": "webp", "ico": "ico", "jpg": "jpg"}[kind]
        sid = slug(row["service_id"])
        source_rel = f"source/original/{sid}.{ext}"
        (out / source_rel).write_bytes(result["content"])
        image_href = svg_data_url(result["content"], kind)
        normalized = _svg_shell(
            f'<image href="{image_href}" x="96" y="96" width="320" height="320" preserveAspectRatio="xMidYMid meet"/>',
            row["display_name"],
        )
        normalized_rel = f"normalized/{sid}.svg"
        (out / normalized_rel).write_text(normalized, encoding="utf-8")
        variants = {
            "source_original": {"path": source_rel, "digest": result["source_digest"], "source_kind": kind}
        }
        for style in STYLE_VARIANTS:
            rendered = render_variant(image_href, row["display_name"], style)
            rel = f"styles/{style}/{sid}.svg"
            (out / rel).write_text(rendered, encoding="utf-8")
            variants[style] = {"path": rel, "digest": sha256(rendered)}

        results.append({
            **row,
            "icon_identity": f"service:{row['service_id']}",
            "source": {
                "origin": "official",
                "homepage_url": result["homepage_url"],
                "source_url": result["source_url"],
                "content_type": result.get("content_type"),
                "digest": result["source_digest"],
                "rights_basis": "official_site_asset",
                "redistribution_status": "review",
                "resolution_reason": result["resolution_reason"],
                "homepage_digest": result.get("homepage_digest"),
            },
            "normalized": {"path": normalized_rel, "digest": sha256(normalized)},
            "variants": variants,
            "lineage": {
                **lineage,
                "source_digest": result["source_digest"],
                "renderer_version": RENDERER_VERSION,
            },
            "release_eligible": True,
        })

    for style in STYLE_VARIANTS:
        write_preview(style, results, out)

    complete = sum(1 for row in results if row.get("release_eligible") and all(k in row.get("variants", {}) for k in VARIANTS))
    missing = [row["service_id"] for row in results if not all(k in row.get("variants", {}) for k in VARIANTS)]
    manifest = {
        "schema": "icon_registry_v5",
        "version": 5,
        "renderer_version": RENDERER_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "run_id": lineage["run_id"],
        "snapshot_id": lineage["snapshot_id"],
        "ir_digest": lineage["ir_digest"],
        "service_universe": {"source": str(rule_index), "count": len(entries)},
        "variants": list(VARIANTS),
        "entries": results,
        "coverage": {
            "service_count": len(entries),
            "icon_identity_count": sum(1 for x in results if x.get("source", {}).get("digest")),
            "complete_8_of_8": complete,
            "missing": missing,
            "orphans": [],
        },
        "acquisition": {
            "unique_source_urls": len(acquired_by_url),
            "network_policy": "one_asset_fetch_per_run",
        },
    }
    (out / "registry.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out / "release-pointer.json").write_text(
        json.dumps({
            "schema": "icon_release_pointer_v5",
            "status": "candidate" if missing else "rc_ready",
            "registry": "registry.json",
            "renderer_version": RENDERER_VERSION,
            "run_id": lineage["run_id"],
            "snapshot_id": lineage["snapshot_id"],
            "ir_digest": lineage["ir_digest"],
        }, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "status": "ok" if (not args.strict or not missing) else "blocked",
        "service_count": len(entries),
        "complete_8_of_8": complete,
        "missing": missing,
        "unique_source_urls": len(acquired_by_url),
        "out": str(out),
    }, ensure_ascii=False))
    return 0 if (not args.strict or not missing) else 1


def gate(args: argparse.Namespace) -> int:
    registry_path = Path(args.registry)
    registry = load_json(registry_path)
    errors = []
    if registry.get("schema") != "icon_registry_v5":
        errors.append("schema mismatch")
    if registry.get("variants") != list(VARIANTS):
        errors.append("eight-layer variant contract mismatch")
    entries = registry.get("entries") or []
    ids = [str(x.get("service_id") or "") for x in entries]
    if len(ids) != len(set(ids)):
        errors.append("duplicate service_id in registry")
    for row in entries:
        sid = row.get("service_id")
        if row.get("release_eligible") is not True:
            if args.strict:
                errors.append(f"{sid}: not release eligible")
            continue
        source = row.get("source") or {}
        digest = str(source.get("digest") or "")
        if not re.fullmatch(r"[0-9a-f]{64}", digest):
            errors.append(f"{sid}: invalid source digest")
        for key in VARIANTS:
            item = (row.get("variants") or {}).get(key)
            if not item:
                errors.append(f"{sid}:{key}: missing variant")
                continue
            path = registry_path.parent / str(item.get("path") or "")
            if not path.is_file():
                errors.append(f"{sid}:{key}: missing file")
                continue
            got = sha256(path.read_bytes())
            if got != str(item.get("digest") or ""):
                errors.append(f"{sid}:{key}: digest mismatch")
            if key != "source_original":
                try:
                    root = ET.fromstring(path.read_text(encoding="utf-8"))
                    if root.tag.rsplit("}", 1)[-1] != "svg":
                        raise ValueError("not svg")
                except Exception as exc:
                    errors.append(f"{sid}:{key}: invalid svg: {exc}")
        lin = row.get("lineage") or {}
        for field in ("run_id", "renderer_version"):
            if not str(lin.get(field) or "").strip():
                errors.append(f"{sid}: missing lineage {field}")
    coverage = registry.get("coverage") or {}
    if args.strict and int(coverage.get("complete_8_of_8") or 0) != int(coverage.get("service_count") or 0):
        errors.append("8/8 coverage incomplete")
    report = {"schema": "icon_v5_gate_v1", "status": "PASS" if not errors else "FAIL", "errors": errors}
    out = registry_path.parent / "gate.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0 if not errors else 1


def discover(args: argparse.Namespace) -> int:
    rows = discover_services(Path(args.rule_index))
    doc = load_yaml(Path(args.rule_index))
    result = {
        "schema": "icon_service_discovery_v5",
        "run_id": doc.get("run_id"),
        "ir_digest": doc.get("ir_digest"),
        "service_count": len(rows),
        "services": rows,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "ok", "service_count": len(rows), "out": str(out)}, ensure_ascii=False))
    return 0


def contract() -> int:
    policy = load_yaml(POLICY)
    if policy.get("version") != 5:
        raise SystemExit("icon_v5 policy version mismatch")
    if tuple(policy.get("variants") or []) != VARIANTS:
        raise SystemExit("icon_v5 variant contract mismatch")
    print(json.dumps({"status": "PASS", "schema": "icon_v5_contract_v1", "variants": list(VARIANTS), "renderer_version": RENDERER_VERSION}, ensure_ascii=False))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="command", required=True)
    sub.add_parser("contract")
    p = sub.add_parser("discover")
    p.add_argument("--rule-index", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p = sub.add_parser("build")
    p.add_argument("--rule-index", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--run-id")
    p.add_argument("--snapshot-id")
    p.add_argument("--ir-digest")
    p.add_argument("--strict", action="store_true")
    p = sub.add_parser("gate")
    p.add_argument("--registry", type=Path, required=True)
    p.add_argument("--strict", action="store_true")
    args = ap.parse_args()
    if args.command == "contract":
        return contract()
    if args.command == "discover":
        return discover(args)
    if args.command == "build":
        return build(args)
    if args.command == "gate":
        return gate(args)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
