#!/usr/bin/env python3
"""Icon System V5: quality-aware source acquisition, eight-layer registry and gates.

Source First → Quality Gating → Seed Fallback → Render → Limited Post-process.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener
import xml.etree.ElementTree as ET

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.icon_v5_renderers import RENDERERS
from scripts.icon_v5_renderers.common import svg_data_url

POLICY = ROOT / "config/icon_v5.yaml"
OFFICIAL_SITES = ROOT / "config/official_sites.yaml"
DEFAULT_CACHE = ROOT / "assets/icons/v5/source"
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
RENDERER_VERSION = "prc-icon-renderer-v5.1.0"

# Quality tiers (source_px = max(width, height))
QUALITY_HIGH = "high"
QUALITY_MEDIUM = "medium"
QUALITY_ACCEPTABLE = "acceptable"
QUALITY_LOW = "low_res"

# Default thresholds (overridable via config/icon_v5.yaml quality section)
DEFAULT_MIN_SOURCE_PX = 96
DEFAULT_PREFERRED_SOURCE_PX = 128


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


def quality_from_px(source_px: int, *, min_px: int = DEFAULT_MIN_SOURCE_PX) -> str:
    if source_px <= 0:
        return QUALITY_LOW
    if source_px >= 256:
        return QUALITY_HIGH
    if source_px >= 128:
        return QUALITY_MEDIUM
    if source_px >= min_px:
        return QUALITY_ACCEPTABLE
    return QUALITY_LOW


def quality_rank(q: str) -> int:
    return {
        QUALITY_HIGH: 4,
        QUALITY_MEDIUM: 3,
        QUALITY_ACCEPTABLE: 2,
        QUALITY_LOW: 1,
    }.get(q, 0)


# ---------------------------------------------------------------------------
# Raster / ICO / SVG dimension inspection
# ---------------------------------------------------------------------------

def _pil_open(content: bytes):
    try:
        from PIL import Image
    except ImportError:
        return None
    try:
        return Image.open(io.BytesIO(content))
    except Exception:
        return None


def extract_best_ico_frame(content: bytes) -> tuple[bytes, int, int, int]:
    """Return (png_bytes, width, height, frame_count) for the largest ICO frame."""
    im = _pil_open(content)
    if im is None:
        return content, 0, 0, 0
    frames: list[tuple[int, int, int, object]] = []
    n = getattr(im, "n_frames", 1) or 1
    for i in range(n):
        try:
            im.seek(i)
            w, h = im.size
            area = int(w) * int(h)
            if area <= 0:
                continue
            frames.append((area, int(w), int(h), im.copy()))
        except Exception:
            continue
    if not frames:
        w, h = im.size
        return content, int(w), int(h), n
    frames.sort(key=lambda x: (x[0], x[1], x[2]), reverse=True)
    _, w, h, frame = frames[0]
    buf = io.BytesIO()
    # Prefer RGBA PNG for embed stability
    if frame.mode not in ("RGBA", "RGB"):
        frame = frame.convert("RGBA")
    elif frame.mode == "RGB":
        frame = frame.convert("RGBA")
    frame.save(buf, format="PNG")
    return buf.getvalue(), w, h, n


def inspect_source_bytes(content: bytes, content_type: str | None, kind_hint: str | None = None) -> dict:
    """Decode content and return kind, width, height, source_px, optionally normalized PNG for ICO."""
    kind = kind_hint or "bin"
    if content_type:
        ct = content_type.split(";")[0].strip().lower()
        if "svg" in ct:
            kind = "svg"
        elif "png" in ct:
            kind = "png"
        elif "webp" in ct:
            kind = "webp"
        elif "icon" in ct or "x-icon" in ct:
            kind = "ico"
        elif "jpeg" in ct or "jpg" in ct:
            kind = "jpg"
    if kind == "bin":
        if content[:4] == b"\x00\x00\x01\x00":
            kind = "ico"
        elif content.startswith(b"\x89PNG\r\n\x1a\n"):
            kind = "png"
        elif content.startswith(b"<svg") or content.lstrip().startswith(b"<?xml") or b"<svg" in content[:200]:
            kind = "svg"
        elif content[:3] == b"GIF":
            kind = "gif"
        elif content[:2] == b"\xff\xd8":
            kind = "jpg"

    width = height = 0
    frame_count = 1
    normalized_content = content
    normalized_kind = kind

    if kind == "svg":
        # Vector: treat as high-quality infinite resolution for gating
        width = height = 512
        try:
            text = content.decode("utf-8", errors="ignore")
            m = re.search(r'viewBox\s*=\s*["\']\s*([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)', text, re.I)
            if m:
                width = max(int(float(m.group(3))), 1)
                height = max(int(float(m.group(4))), 1)
            else:
                mw = re.search(r'\bwidth\s*=\s*["\']?(\d+)', text, re.I)
                mh = re.search(r'\bheight\s*=\s*["\']?(\d+)', text, re.I)
                if mw and mh:
                    width = int(mw.group(1))
                    height = int(mh.group(1))
        except Exception:
            width = height = 512
        # Cap reported px for SVG as high (vector)
        source_px = max(width, height, 256)
        return {
            "kind": "svg",
            "width": width,
            "height": height,
            "source_px": source_px,
            "frame_count": 1,
            "selected_frame": f"{width}x{height}",
            "content": content,
            "embed_kind": "svg",
            "is_vector": True,
        }

    if kind == "ico":
        png, w, h, n = extract_best_ico_frame(content)
        return {
            "kind": "ico",
            "width": w,
            "height": h,
            "source_px": max(w, h),
            "frame_count": n,
            "selected_frame": f"{w}x{h}",
            "content": png if w > 0 else content,
            "embed_kind": "png" if w > 0 else "ico",
            "is_vector": False,
        }

    im = _pil_open(content)
    if im is not None:
        width, height = im.size
        return {
            "kind": kind,
            "width": int(width),
            "height": int(height),
            "source_px": max(int(width), int(height)),
            "frame_count": 1,
            "selected_frame": f"{width}x{height}",
            "content": content,
            "embed_kind": kind if kind in ("png", "webp", "jpg", "svg") else "png",
            "is_vector": False,
        }

    return {
        "kind": kind,
        "width": 0,
        "height": 0,
        "source_px": 0,
        "frame_count": 1,
        "selected_frame": "0x0",
        "content": content,
        "embed_kind": kind,
        "is_vector": False,
    }


def candidate_type_score(url: str, kind: str, is_vector: bool, source_px: int, *, from_apple: bool = False, from_manifest: bool = False, direct: bool = False) -> int:
    """Higher is better. Aligns with plan section 7."""
    score = 0
    if is_vector or kind == "svg":
        score += 100
    elif from_apple:
        score += 90
    elif kind == "png" and source_px >= 256:
        score += 85
    elif kind == "png" and source_px >= 128:
        score += 75
    elif kind in ("ico", "png", "webp", "jpg") and source_px >= 128:
        score += 70
    elif source_px >= 96:
        score += 60
    elif source_px >= 48:
        score += 40
    elif source_px >= 32:
        score += 20
    else:
        score += 5
    if direct:
        score += 15
    if from_manifest:
        score += 8
    # Prefer apple-touch in URL
    ul = url.lower()
    if "apple-touch" in ul:
        score += 12
    if ul.endswith(".svg") or "svg" in ul:
        score += 10
    if "favicon" in ul and source_px < 96:
        score -= 10
    return score


# ---------------------------------------------------------------------------
# Discovery helpers (unchanged core)
# ---------------------------------------------------------------------------

def discover_services_from_rule_index(rule_index: Path) -> list[dict]:
    doc = load_yaml(rule_index)
    rows = []
    seen = set()
    for item in doc.get("entries") or []:
        if not isinstance(item, dict) or item.get("entity") != "service":
            continue
        sid = str(item.get("id") or "").strip()
        if not sid:
            continue
        if sid in seen:
            raise ValueError(f"duplicate service_id in rule index: {sid}")
        seen.add(sid)
        rows.append(
            {
                "service_id": sid,
                "display_name": str(item.get("display_name") or sid),
                "provider": item.get("provider"),
                "rule_path": str(item.get("path") or ""),
                "rule_count": int(item.get("rule_count") or 0),
            }
        )
    if not rows:
        raise ValueError("no service entities discovered")
    return sorted(rows, key=lambda x: x["service_id"])


def discover_services_from_ir(ir_path: Path) -> list[dict]:
    doc = load_json(ir_path)
    entities = doc.get("entities") or doc.get("entity") or {}
    service_ids = entities.get("services") if isinstance(entities, dict) else []
    views = doc.get("views") or {}
    catalog = views.get("service_catalog") if isinstance(views, dict) else None
    by_id = {}
    if isinstance(catalog, list):
        for item in catalog:
            if isinstance(item, dict) and item.get("service_id"):
                by_id[str(item["service_id"])] = item
    rows = []
    for sid in service_ids or list(by_id):
        sid = str(sid)
        meta = by_id.get(sid) or {}
        rows.append(
            {
                "service_id": sid,
                "display_name": str(meta.get("display_name") or sid),
                "provider": meta.get("provider"),
                "rule_path": str(meta.get("path") or ""),
                "rule_count": int(meta.get("rule_count") or 0),
            }
        )
    if not rows:
        raise ValueError("no services in IR")
    return sorted(rows, key=lambda x: x["service_id"])


def candidate_domains(root: Path, row: dict) -> list[tuple[str, int]]:
    path = root / "rule" / str(row.get("rule_path") or "")
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8", errors="ignore")
    counts: dict[str, int] = {}
    for match in re.finditer(r"(?i)(?:^|\s)(?:DOMAIN(?:-SUFFIX)?|HOST)\s*,\s*([a-z0-9.-]+\.[a-z]{2,})", text):
        host = match.group(1).lower().strip(".")
        if host.count(".") >= 1:
            counts[host] = counts.get(host, 0) + 1
    return sorted(counts.items(), key=lambda x: (-x[1], x[0]))


class IconLinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[dict] = []
        self.manifest: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        ad = {k.lower(): (v or "") for k, v in attrs}
        if tag.lower() != "link":
            return
        rel = ad.get("rel", "").lower()
        href = ad.get("href", "").strip()
        if not href:
            return
        if "manifest" in rel:
            self.manifest = href
            return
        sizes = ad.get("sizes", "")
        priority = 50
        if "apple-touch-icon" in rel:
            priority = 10
        elif "icon" in rel and "mask" not in rel:
            if href.lower().endswith(".svg") or "svg" in ad.get("type", "").lower():
                priority = 5
            elif "apple-touch" in href.lower():
                priority = 10
            else:
                priority = 20
        elif "shortcut icon" in rel or rel == "icon":
            priority = 30
        self.links.append({"href": href, "rel": rel, "sizes": sizes, "priority": priority, "type": ad.get("type", "")})


class LimitedRedirectHandler(HTTPRedirectHandler):
    def __init__(self, max_redirects: int = 5):
        super().__init__()
        self.max_redirects = max_redirects
        self.redirects = 0

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.redirects += 1
        if self.redirects > self.max_redirects:
            raise RuntimeError(f"too many redirects (>{self.max_redirects})")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch_bytes(url: str, *, timeout: int, max_bytes: int, user_agent: str, max_redirects: int, accept: str) -> tuple[bytes, dict]:
    if not url.lower().startswith("https://"):
        raise ValueError(f"non-https url rejected: {url}")
    handler = LimitedRedirectHandler(max_redirects=max_redirects)
    opener = build_opener(handler)
    req = Request(url, headers={"User-Agent": user_agent, "Accept": accept})
    with opener.open(req, timeout=timeout) as resp:
        data = resp.read(max_bytes + 1)
        if len(data) > max_bytes:
            raise ValueError(f"response exceeds max_bytes={max_bytes}")
        headers = {k.lower(): v for k, v in resp.headers.items()}
        headers["final_url"] = resp.geturl()
        headers["status"] = str(getattr(resp, "status", 200))
        return data, headers


def validate_source(content: bytes, content_type: str | None, url: str) -> str:
    kind = "bin"
    if content_type:
        ct = content_type.split(";")[0].strip().lower()
        allowed = {
            "image/svg+xml": "svg",
            "image/png": "png",
            "image/webp": "webp",
            "image/x-icon": "ico",
            "image/vnd.microsoft.icon": "ico",
            "image/jpeg": "jpg",
        }
        kind = allowed.get(ct, "bin")
    if kind == "bin":
        if content.startswith(b"<svg") or b"<svg" in content[:200]:
            kind = "svg"
        elif content.startswith(b"\x89PNG\r\n\x1a\n"):
            kind = "png"
        elif content[:4] == b"\x00\x00\x01\x00":
            kind = "ico"
        elif content[:2] == b"\xff\xd8":
            kind = "jpg"
        else:
            raise ValueError(f"unsupported content at {url}")
    if kind == "svg":
        text = content.decode("utf-8", errors="ignore")
        lower = text.lower()
        for token in ("<script", "<foreignobject", "<iframe", "<object", "<embed"):
            if token in lower:
                raise ValueError(f"svg contains forbidden element: {token}")
        if re.search(r'href\s*=\s*["\']https?://', text, re.I) and "data:" not in text[:50]:
            # external refs in svg — soft allow data embeds only is preferred; reject obvious remote
            pass
        ET.fromstring(text)
    return kind


def semantic_glyph_svg(service_id: str, display_name: str = "") -> bytes:
    title = (display_name or service_id)[:32]
    letter = (title[:1] or "?").upper()
    colors = ["#4F46E5", "#0EA5E9", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6", "#06B6D4", "#84CC16"]
    color = colors[sum(ord(c) for c in service_id) % len(colors)]
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" role="img" aria-label="{title}">
  <rect width="512" height="512" rx="96" fill="{color}"/>
  <text x="256" y="310" text-anchor="middle" font-family="system-ui,sans-serif" font-size="220" font-weight="700" fill="#ffffff">{letter}</text>
</svg>
'''
    return svg.encode("utf-8")


def try_local_seed(root: Path, sid: str) -> dict | None:
    """Reviewed local seed under assets/icons/seed (or legacy normalized)."""
    for base in (root / "assets" / "icons" / "seed", root / "assets" / "icons" / "normalized"):
        for ext, kind in (("svg", "svg"), ("png", "png"), ("ico", "ico"), ("webp", "webp")):
            p = base / f"{sid}.{ext}"
            if not p.is_file():
                continue
            content = p.read_bytes()
            try:
                validate_source(content, None, str(p))
            except Exception:
                if kind != "svg":
                    continue
            info = inspect_source_bytes(content, None, kind)
            q = quality_from_px(info["source_px"] if not info.get("is_vector") else 512)
            return {
                "status": "ok",
                "content": info["content"],
                "cached": False,
                "service_id": sid,
                "homepage_url": "",
                "source_url": f"seed://{p.relative_to(root)}",
                "source_kind": info["embed_kind"],
                "content_type": {
                    "svg": "image/svg+xml",
                    "png": "image/png",
                    "ico": "image/x-icon",
                    "webp": "image/webp",
                    "jpg": "image/jpeg",
                }.get(info["embed_kind"], "application/octet-stream"),
                "source_digest": sha256(info["content"]),
                "resolution_reason": "reviewed_local_seed",
                "http_status": 200,
                "content_length": str(len(info["content"])),
                "fetched_at": datetime.now(timezone.utc).isoformat(),
                "source_px": info["source_px"],
                "width": info["width"],
                "height": info["height"],
                "quality": q if not info.get("is_vector") else QUALITY_HIGH,
                "source_type": "seed",
                "official": False,
                "fallback": True,
                "seed": True,
                "frame_count": info.get("frame_count", 1),
                "selected_frame": info.get("selected_frame"),
                "is_vector": bool(info.get("is_vector")),
                "score": 200 if info.get("is_vector") else 80 + min(info["source_px"], 256) // 4,
            }
    return None


def select_manifest_icon(base_url: str, data: bytes) -> list[str]:
    try:
        doc = json.loads(data.decode("utf-8"))
    except Exception:
        return []
    candidates = []
    for item in (doc.get("icons") if isinstance(doc, dict) else None) or []:
        if not isinstance(item, dict) or not item.get("src"):
            continue
        area = 0
        for token in str(item.get("sizes") or "").split():
            if "x" not in token:
                continue
            try:
                a, b = token.lower().split("x", 1)
                area = max(area, int(a) * int(b))
            except Exception:
                pass
        candidates.append((area, str(item["src"])))
    candidates.sort(key=lambda x: (-x[0], x[1]))
    return [urljoin(base_url, src) for _, src in candidates]


def load_cache(cache_dir: Path) -> dict:
    path = cache_dir / "cache.json"
    if not path.is_file():
        return {}
    try:
        doc = load_json(path)
    except Exception:
        return {}
    return doc.get("services") if isinstance(doc.get("services"), dict) else {}


def save_cache(cache_dir: Path, services: dict) -> None:
    cache_dir.mkdir(parents=True, exist_ok=True)
    (cache_dir / "cache.json").write_text(
        json.dumps(
            {
                "schema": "icon_source_cache_v5",
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "services": services,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def _normalize_official(official: dict) -> dict:
    return {str(k).strip(): v for k, v in (official or {}).items()}


def _official_entry(official: dict, sid: str) -> tuple[str, str | None]:
    raw = official.get(str(sid))
    if raw is None:
        return "", None
    if isinstance(raw, dict):
        homepage = str(raw.get("homepage") or raw.get("url") or "").strip()
        icon = str(raw.get("icon_url") or raw.get("icon") or "").strip() or None
        return homepage, icon
    return str(raw or "").strip(), None


def _quality_cfg(policy: dict) -> dict:
    q = policy.get("quality") if isinstance(policy.get("quality"), dict) else {}
    return {
        "min_source_px": int(q.get("min_source_px", DEFAULT_MIN_SOURCE_PX)),
        "preferred_source_px": int(q.get("preferred_source_px", DEFAULT_PREFERRED_SOURCE_PX)),
        "reject_below_min": bool(q.get("reject_below_min", True)),
        "seed_beats_low_res": bool(q.get("seed_beats_low_res", True)),
        "core_services_fail_low_res": list(q.get("core_services_fail_low_res") or []),
        "warn_low_res": bool(q.get("warn_low_res", True)),
    }


def resolve_source(root: Path, row: dict, official: dict, policy: dict, cache: dict, asset_cache: dict, *, refresh: bool) -> dict:
    """Quality-aware acquisition: score all candidates, reject <min_px unless no better option."""
    sid = row["service_id"]
    qcfg = _quality_cfg(policy)
    min_px = qcfg["min_source_px"]

    # Cache only if quality metadata present and not low_res (or refresh)
    cached = None if refresh else cache.get(sid)
    if cached and cached.get("source_url"):
        path = ROOT / str(cached.get("path") or "")
        if path.is_file() and sha256(path.read_bytes()) == str(cached.get("digest") or ""):
            content = path.read_bytes()
            cq = str(cached.get("quality") or "")
            if cq and quality_rank(cq) >= quality_rank(QUALITY_ACCEPTABLE):
                return {**cached, "status": "ok", "content": content, "cached": True}

    seed = try_local_seed(ROOT, sid)
    homepage, direct_icon = _official_entry(official, sid)

    if sid in official and not homepage and not direct_icon:
        if seed:
            return seed
        content = semantic_glyph_svg(sid, str(row.get("display_name") or sid))
        return _glyph_result(sid, content, row)

    if not homepage and not direct_icon:
        candidates_dom = candidate_domains(root, row)
        if not candidates_dom or candidates_dom[0][1] < 2:
            if seed:
                return seed
            return {"status": "hold", "reason": "no_high_confidence_official_homepage_candidate"}
        homepage = "https://" + candidates_dom[0][0] + "/"
        reason = "rule_domain_candidate"
    else:
        reason = "registered_official" if homepage or direct_icon else "unknown"

    acq = policy["acquisition"]
    timeout = int(acq.get("timeout_seconds", 25))
    max_redirects = int(acq.get("max_redirects", 5))
    max_bytes = int(acq.get("max_bytes", 1048576))
    page_max = int(acq.get("page_max_bytes", max_bytes * 3))
    user_agent = str(acq.get("user_agent", "Popular-Rules-Collection/Icon-System-V5"))

    # Build ordered URL list (discovery); scoring happens after download
    url_specs: list[dict] = []

    def add_url(u: str, *, direct: bool = False, from_apple: bool = False, from_manifest: bool = False, hint_priority: int = 50):
        if not u or not u.lower().startswith("https://"):
            return
        if any(x["url"] == u for x in url_specs):
            return
        url_specs.append(
            {
                "url": u,
                "direct": direct,
                "from_apple": from_apple or ("apple-touch" in u.lower()),
                "from_manifest": from_manifest,
                "hint_priority": hint_priority,
            }
        )

    if direct_icon:
        add_url(direct_icon, direct=True, hint_priority=1)

    page_headers = {"final_url": homepage or ""}
    if homepage:
        try:
            page, page_headers = fetch_bytes(
                homepage,
                timeout=timeout,
                max_bytes=page_max,
                user_agent=user_agent,
                max_redirects=max_redirects,
                accept="text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
            )
            parser = IconLinkParser()
            parser.feed(page.decode("utf-8", errors="ignore"))
            for link in sorted(parser.links, key=lambda x: (x["priority"], x["sizes"] or "", x["href"])):
                u = urljoin(page_headers["final_url"], link["href"])
                add_url(
                    u,
                    from_apple="apple-touch" in link.get("rel", ""),
                    hint_priority=int(link.get("priority") or 50),
                )
            if parser.manifest:
                try:
                    manifest_url = urljoin(page_headers["final_url"], parser.manifest)
                    mdata, _ = fetch_bytes(
                        manifest_url,
                        timeout=timeout,
                        max_bytes=max_bytes,
                        user_agent=user_agent,
                        max_redirects=max_redirects,
                        accept="application/manifest+json,application/json,*/*;q=0.8",
                    )
                    for mu in select_manifest_icon(manifest_url, mdata):
                        add_url(mu, from_manifest=True, hint_priority=15)
                except Exception:
                    pass
        except Exception:
            pass

        base = page_headers.get("final_url") or homepage
        # Prefer high-quality well-known paths before generic favicon
        for rel, hp in (
            ("/apple-touch-icon.png", 10),
            ("/apple-touch-icon-precomposed.png", 11),
            ("/apple-touch-icon-180x180.png", 9),
            ("/icon.svg", 6),
            ("/logo.svg", 7),
            ("/favicon.svg", 8),
            ("/favicon-32x32.png", 35),
            ("/favicon-96x96.png", 25),
            ("/favicon-128x128.png", 22),
            ("/favicon-192x192.png", 18),
            ("/favicon-512x512.png", 16),
            ("/favicon.png", 40),
            ("/favicon.ico", 45),
            ("/static/favicon.ico", 46),
        ):
            add_url(urljoin(base, rel), from_apple="apple-touch" in rel, hint_priority=hp)

    # Download and score candidates
    scored: list[dict] = []
    last_err: Exception | None = None
    for spec in sorted(url_specs, key=lambda x: x["hint_priority"]):
        url = spec["url"]
        try:
            data, headers = fetch_bytes(
                url,
                timeout=timeout,
                max_bytes=max_bytes,
                user_agent=user_agent,
                max_redirects=max_redirects,
                accept="image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
            )
            ctype = headers.get("content-type")
            kind = validate_source(data, ctype, url)
            info = inspect_source_bytes(data, ctype, kind)
            spx = info["source_px"]
            is_vec = bool(info.get("is_vector"))
            q = QUALITY_HIGH if is_vec else quality_from_px(spx, min_px=min_px)
            score = candidate_type_score(
                url,
                info["embed_kind"],
                is_vec,
                spx,
                from_apple=spec["from_apple"],
                from_manifest=spec["from_manifest"],
                direct=spec["direct"],
            )
            # Reject below min unless we keep as last-resort low_res
            if qcfg["reject_below_min"] and not is_vec and spx < min_px:
                scored.append(
                    {
                        "rejected": True,
                        "reason": f"below_min_source_px:{spx}<{min_px}",
                        "url": url,
                        "source_px": spx,
                        "quality": q,
                        "score": score - 50,
                        "info": info,
                        "headers": headers,
                        "kind": kind,
                    }
                )
                continue
            scored.append(
                {
                    "rejected": False,
                    "url": url,
                    "source_px": spx,
                    "quality": q,
                    "score": score,
                    "info": info,
                    "headers": headers,
                    "kind": kind,
                    "resolution_reason": reason,
                }
            )
        except Exception as exc:
            last_err = exc
            continue

    accepted = [c for c in scored if not c.get("rejected")]
    accepted.sort(key=lambda c: (-c["score"], -c["source_px"], c["url"]))

    best = accepted[0] if accepted else None

    # Seed beats low_res / weaker network source
    if seed and qcfg["seed_beats_low_res"]:
        if best is None:
            return seed
        if quality_rank(str(seed.get("quality"))) > quality_rank(str(best.get("quality"))):
            return seed
        if quality_rank(str(best.get("quality"))) <= quality_rank(QUALITY_LOW):
            return seed
        if seed.get("is_vector") and not best.get("info", {}).get("is_vector"):
            if quality_rank(str(best.get("quality"))) < quality_rank(QUALITY_HIGH):
                return seed

    if best is not None:
        info = best["info"]
        return {
            "status": "ok",
            "content": info["content"],
            "cached": False,
            "service_id": sid,
            "homepage_url": page_headers.get("final_url") or homepage or "",
            "source_url": best["url"],
            "source_kind": info["embed_kind"],
            "content_type": best["headers"].get("content-type"),
            "source_digest": sha256(info["content"]),
            "resolution_reason": best.get("resolution_reason") or reason,
            "http_status": int(best["headers"].get("status") or 200),
            "content_length": str(len(info["content"])),
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "source_px": info["source_px"],
            "width": info["width"],
            "height": info["height"],
            "quality": best["quality"],
            "source_type": info["kind"],
            "official": True,
            "fallback": False,
            "seed": False,
            "frame_count": info.get("frame_count", 1),
            "selected_frame": info.get("selected_frame"),
            "is_vector": bool(info.get("is_vector")),
            "score": best["score"],
        }

    # All network rejected or failed — use best rejected only if no seed
    rejected_ok = [c for c in scored if c.get("rejected")]
    rejected_ok.sort(key=lambda c: (-c["source_px"], -c["score"]))
    if seed:
        return seed
    if rejected_ok:
        # Last resort: low_res network
        best = rejected_ok[0]
        info = best["info"]
        return {
            "status": "ok",
            "content": info["content"],
            "cached": False,
            "service_id": sid,
            "homepage_url": page_headers.get("final_url") or homepage or "",
            "source_url": best["url"],
            "source_kind": info["embed_kind"],
            "content_type": best["headers"].get("content-type"),
            "source_digest": sha256(info["content"]),
            "resolution_reason": "low_res_last_resort",
            "http_status": int(best["headers"].get("status") or 200),
            "content_length": str(len(info["content"])),
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "source_px": info["source_px"],
            "width": info["width"],
            "height": info["height"],
            "quality": QUALITY_LOW,
            "source_type": info["kind"],
            "official": True,
            "fallback": True,
            "seed": False,
            "frame_count": info.get("frame_count", 1),
            "selected_frame": info.get("selected_frame"),
            "is_vector": False,
            "score": best["score"],
        }

    content = semantic_glyph_svg(sid, str(row.get("display_name") or sid))
    out = _glyph_result(sid, content, row)
    out["prior_failure"] = f"{type(last_err).__name__ if last_err else 'none'}: {last_err}"
    return out


def _glyph_result(sid: str, content: bytes, row: dict) -> dict:
    return {
        "status": "ok",
        "content": content,
        "cached": False,
        "service_id": sid,
        "homepage_url": "",
        "source_url": f"semantic://glyph/{sid}",
        "source_kind": "svg",
        "content_type": "image/svg+xml",
        "source_digest": sha256(content),
        "resolution_reason": "semantic_fallback_glyph",
        "http_status": 200,
        "content_length": str(len(content)),
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "source_px": 512,
        "width": 512,
        "height": 512,
        "quality": QUALITY_MEDIUM,
        "source_type": "glyph",
        "official": False,
        "fallback": True,
        "seed": False,
        "frame_count": 1,
        "selected_frame": "512x512",
        "is_vector": True,
        "score": 30,
    }


def acquire_source(row: dict, official: dict, policy: dict, cache: dict, cache_dir: Path, asset_cache: dict, *, refresh: bool) -> dict:
    result = resolve_source(ROOT, row, official, policy, cache, asset_cache, refresh=refresh)
    if result.get("status") != "ok":
        return result
    if result.get("cached"):
        return result
    ext = {"svg": "svg", "png": "png", "webp": "webp", "ico": "ico", "jpg": "jpg"}.get(result["source_kind"], "bin")
    path = cache_dir / (slug(row["service_id"]) + "." + ext)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(result["content"])
    meta = {
        k: result.get(k)
        for k in (
            "source_url",
            "homepage_url",
            "source_kind",
            "content_type",
            "resolution_reason",
            "http_status",
            "content_length",
            "fetched_at",
            "source_px",
            "width",
            "height",
            "quality",
            "source_type",
            "official",
            "fallback",
            "seed",
            "frame_count",
            "selected_frame",
            "is_vector",
            "score",
        )
    }
    meta.update({"path": str(path.relative_to(ROOT)), "digest": result["source_digest"], "service_id": row["service_id"]})
    cache[row["service_id"]] = meta
    return result


def render_pngs(svg: str, out_root: Path, service_id: str, variant: str, sizes: list[int]) -> dict[str, str]:
    import cairosvg

    paths: dict[str, str] = {}
    for size in sizes:
        path = out_root / "png" / str(size) / variant / (slug(service_id) + ".png")
        path.parent.mkdir(parents=True, exist_ok=True)
        cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=str(path), output_width=size, output_height=size)
        paths[str(size)] = str(path.relative_to(out_root))
    return paths


# Styles that are gentler on low-res subjects
LOW_RES_PREFERRED_STYLES = ("minimalist", "duotone_line", "source_original")


def cmd_contract(_: argparse.Namespace) -> int:
    policy = load_yaml(POLICY)
    required = [
        "schema",
        "coverage",
        "identity",
        "variants",
        "acquisition",
        "render",
        "lineage",
        "release",
    ]
    missing = [k for k in required if k not in policy]
    if missing:
        print(json.dumps({"status": "fail", "missing": missing}, ensure_ascii=False))
        return 1
    print(json.dumps({"status": "ok", "schema": policy.get("schema"), "renderer": RENDERER_VERSION}, ensure_ascii=False))
    return 0


def cmd_discover(args: argparse.Namespace) -> int:
    if args.rule_index:
        rows = discover_services_from_rule_index(Path(args.rule_index))
    else:
        rows = discover_services_from_ir(Path(args.ir))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": "icon_service_discovery_v5",
        "count": len(rows),
        "services": rows,
    }
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "ok", "count": len(rows), "out": str(out)}, ensure_ascii=False))
    return 0


def cmd_build(args: argparse.Namespace) -> int:
    policy, official = load_yaml(POLICY), _normalize_official(load_yaml(OFFICIAL_SITES))
    if args.rule_index:
        rows = discover_services_from_rule_index(Path(args.rule_index))
    else:
        rows = discover_services_from_ir(Path(args.ir))
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    cache_dir = Path(args.cache_dir) if args.cache_dir else DEFAULT_CACHE
    cache = load_cache(cache_dir)
    asset_cache: dict = {}
    lineage = {
        "run_id": str(args.run_id or ""),
        "snapshot_id": str(args.snapshot_id or ""),
        "ir_digest": str(args.ir_digest or ""),
    }
    if args.run_manifest:
        run_manifest = load_json(Path(args.run_manifest))
        ir_manifest = load_json(Path(args.ir_manifest)) if args.ir_manifest else {}
        lineage["run_id"] = lineage["run_id"] or str(run_manifest.get("run_id") or "")
        lineage["snapshot_id"] = lineage["snapshot_id"] or str(run_manifest.get("snapshot_id") or "")
        lineage["ir_digest"] = lineage["ir_digest"] or str(ir_manifest.get("ir_digest") or "")
    if args.rule_index:
        doc = load_yaml(Path(args.rule_index))
        lineage["run_id"] = lineage["run_id"] or str(doc.get("run_id") or "")
        lineage["ir_digest"] = lineage["ir_digest"] or str(doc.get("ir_digest") or "")
        lineage["snapshot_id"] = lineage["snapshot_id"] or str(doc.get("snapshot_id") or doc.get("run_id") or "bootstrap-rule-index")
    if args.ir:
        doc = load_json(Path(args.ir))
        meta = doc.get("metadata") if isinstance(doc.get("metadata"), dict) else {}
        lineage["run_id"] = lineage["run_id"] or str(doc.get("run_id") or meta.get("run_id") or "")
        lineage["snapshot_id"] = lineage["snapshot_id"] or str(doc.get("snapshot_id") or meta.get("snapshot_id") or "")
        lineage["ir_digest"] = lineage["ir_digest"] or str(doc.get("ir_digest") or meta.get("ir_digest") or "")
    if args.rule_index:
        lineage["run_id"] = lineage["run_id"] or "bootstrap-rule-index-run"
        lineage["snapshot_id"] = lineage["snapshot_id"] or lineage["run_id"] or "bootstrap-rule-index"
        lineage["ir_digest"] = lineage["ir_digest"] or "bootstrap-no-ir-digest"
    if args.strict and not all(lineage.values()):
        print(json.dumps({"status": "blocked", "reason": "strict build requires run_id, snapshot_id and ir_digest", "lineage": lineage}, ensure_ascii=False))
        return 1

    results = []
    quality_summary = {QUALITY_HIGH: 0, QUALITY_MEDIUM: 0, QUALITY_ACCEPTABLE: 0, QUALITY_LOW: 0}

    for row in rows:
        try:
            source = acquire_source(row, official, policy, cache, cache_dir, asset_cache, refresh=bool(args.refresh))
            if source.get("status") != "ok":
                results.append(
                    {
                        **row,
                        "icon_identity": f"service:{row['service_id']}",
                        "source": {"origin": "hold", "digest": None, "reason": source.get("reason"), "quality": QUALITY_LOW, "source_px": 0},
                        "variants": {},
                        "lineage": {**lineage, "source_digest": None, "renderer_version": RENDERER_VERSION},
                        "release_eligible": False,
                    }
                )
                continue
            sid = row["service_id"]
            kind = source["source_kind"]
            href = svg_data_url(source["content"], kind if kind in ("svg", "png", "webp", "ico", "jpg") else "png")
            normalized = (
                f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">'
                f'<image href="{href}" x="96" y="96" width="320" height="320" preserveAspectRatio="xMidYMid meet"/></svg>'
            )
            np = out / "normalized" / (sid + ".svg")
            np.parent.mkdir(parents=True, exist_ok=True)
            np.write_text(normalized, encoding="utf-8")
            variants = {}
            q = str(source.get("quality") or QUALITY_MEDIUM)
            quality_summary[q] = quality_summary.get(q, 0) + 1
            # low_res: still render all 8 styles for coverage, but mark preference
            for style, renderer in RENDERERS.items():
                svg = renderer(href, str(row.get("display_name") or sid))
                style_dir = style.replace("_", "-")
                sp = out / "styles" / style_dir / (slug(sid) + ".svg")
                sp.parent.mkdir(parents=True, exist_ok=True)
                sp.write_text(svg, encoding="utf-8")
                variants[style] = {
                    "path": str(sp.relative_to(out)),
                    "digest": sha256(svg),
                    "png": render_pngs(svg, out, row["service_id"], style, list(policy["render"]["png_sizes"])),
                }
            src_meta = {
                "origin": (
                    "official_registered"
                    if source.get("resolution_reason") == "registered_official"
                    else "reviewed_local_seed"
                    if source.get("resolution_reason") == "reviewed_local_seed"
                    else "semantic_fallback"
                    if source.get("resolution_reason") == "semantic_fallback_glyph"
                    else "low_res_last_resort"
                    if source.get("resolution_reason") == "low_res_last_resort"
                    else "official_discovered"
                ),
                "homepage_url": source.get("homepage_url"),
                "source_url": source.get("source_url"),
                "content_type": source.get("content_type"),
                "digest": source.get("source_digest"),
                "rights_basis": (
                    "official_site_asset"
                    if source.get("resolution_reason")
                    in {"registered_official", "rule_domain_candidate", "official_discovered", "low_res_last_resort"}
                    else "reviewed_local_seed"
                    if source.get("resolution_reason") == "reviewed_local_seed"
                    else "semantic_glyph"
                ),
                "redistribution_status": "review",
                "resolution_reason": source.get("resolution_reason"),
                "http_status": source.get("http_status"),
                "content_length": source.get("content_length"),
                "fetched_at": source.get("fetched_at"),
                # Quality metadata (plan §10)
                "source_px": source.get("source_px"),
                "width": source.get("width"),
                "height": source.get("height"),
                "quality": q,
                "source_type": source.get("source_type") or source.get("source_kind"),
                "official": bool(source.get("official")),
                "fallback": bool(source.get("fallback")),
                "seed": bool(source.get("seed")),
                "frame_count": source.get("frame_count"),
                "selected_frame": source.get("selected_frame"),
                "is_vector": bool(source.get("is_vector")),
                "score": source.get("score"),
                "preferred_styles_if_low_res": list(LOW_RES_PREFERRED_STYLES) if q == QUALITY_LOW else None,
            }
            results.append(
                {
                    **row,
                    "icon_identity": f"service:{row['service_id']}",
                    "source": src_meta,
                    "normalized": {"path": str(np.relative_to(out)), "digest": sha256(normalized)},
                    "variants": variants,
                    "lineage": {**lineage, "source_digest": source.get("source_digest"), "renderer_version": RENDERER_VERSION},
                    "release_eligible": True,
                }
            )
        except Exception as exc:
            results.append(
                {
                    **row,
                    "icon_identity": f"service:{row['service_id']}",
                    "source": {"origin": "error", "digest": None, "reason": f"{type(exc).__name__}: {exc}", "quality": QUALITY_LOW, "source_px": 0},
                    "variants": {},
                    "lineage": {**lineage, "source_digest": None, "renderer_version": RENDERER_VERSION},
                    "release_eligible": False,
                }
            )

    save_cache(cache_dir, cache)
    complete = sum(1 for r in results if r.get("release_eligible") and len(r.get("variants") or {}) == 8)
    registry = {
        "schema": "icon_registry_v5",
        "renderer_version": RENDERER_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "lineage": lineage,
        "variants": list(VARIANTS),
        "coverage": {
            "service_count": len(results),
            "complete_8_of_8": complete,
            "missing": [r["service_id"] for r in results if not (r.get("release_eligible") and len(r.get("variants") or {}) == 8)],
            "quality": quality_summary,
            "low_res_services": [r["service_id"] for r in results if (r.get("source") or {}).get("quality") == QUALITY_LOW],
        },
        "entries": results,
        "release_status": "candidate" if complete == len(results) and results else "bootstrap",
    }
    (out / "registry.json").write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    status = "ok" if complete == len(results) else "partial"
    if args.strict and complete != len(results) and not getattr(args, "allow_partial", False):
        status = "blocked"
        print(
            json.dumps(
                {
                    "status": status,
                    "service_count": len(results),
                    "complete_8_of_8": complete,
                    "missing": registry["coverage"]["missing"],
                    "quality": quality_summary,
                    "out": str(out),
                    "allow_partial": False,
                },
                ensure_ascii=False,
            )
        )
        return 1
    print(
        json.dumps(
            {
                "status": status,
                "service_count": len(results),
                "complete_8_of_8": complete,
                "missing": registry["coverage"]["missing"],
                "quality": quality_summary,
                "out": str(out),
                "allow_partial": bool(getattr(args, "allow_partial", False)),
            },
            ensure_ascii=False,
        )
    )
    return 0


def cmd_gate(args: argparse.Namespace) -> int:
    registry = load_json(Path(args.registry))
    policy = load_yaml(POLICY)
    qcfg = _quality_cfg(policy)
    errors: list[str] = []
    warnings: list[str] = []
    if registry.get("schema") != "icon_registry_v5":
        errors.append("invalid schema")
    entries = registry.get("entries") or []
    ids = [e.get("service_id") for e in entries]
    if len(ids) != len(set(ids)):
        errors.append("duplicate service_id")
    if args.rule_index:
        expected = {r["service_id"] for r in discover_services_from_rule_index(Path(args.rule_index))}
        actual = set(ids)
        if expected != actual:
            errors.append(f"coverage mismatch missing={sorted(expected - actual)[:20]} extra={sorted(actual - expected)[:20]}")
    core = set(qcfg.get("core_services_fail_low_res") or [])
    for e in entries:
        sid = e.get("service_id")
        src = e.get("source") or {}
        variants = e.get("variants") or {}
        if args.strict and (not e.get("release_eligible") or len(variants) != 8):
            errors.append(f"{sid}: incomplete variants")
        for key, item in variants.items():
            for size in policy.get("render", {}).get("png_sizes") or [64, 128, 256]:
                png = Path(args.registry).parent / str((item.get("png") or {}).get(str(size)) or "")
                if args.strict and (not png.is_file() or png.stat().st_size <= 100):
                    errors.append(f"{sid}:{key}: missing PNG {size}")
        q = str(src.get("quality") or "")
        spx = int(src.get("source_px") or 0)
        if q == QUALITY_LOW or (spx and spx < qcfg["min_source_px"] and not src.get("is_vector") and not src.get("seed")):
            msg = f"{sid}: low_res source_px={spx} quality={q} url={src.get('source_url')}"
            if sid in core:
                errors.append(msg)
            elif qcfg.get("warn_low_res", True):
                warnings.append(msg)
        if "source_px" not in src and e.get("release_eligible"):
            warnings.append(f"{sid}: missing source_px metadata")
        if "quality" not in src and e.get("release_eligible"):
            warnings.append(f"{sid}: missing quality metadata")
    payload = {
        "schema": "icon_v5_gate_v1",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
        "quality": (registry.get("coverage") or {}).get("quality"),
        "low_res_services": (registry.get("coverage") or {}).get("low_res_services"),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="Icon System V5")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("contract")
    p.set_defaults(func=cmd_contract)
    p = sub.add_parser("discover")
    p.add_argument("--rule-index")
    p.add_argument("--ir")
    p.add_argument("--out", required=True)
    p.set_defaults(func=cmd_discover)
    p = sub.add_parser("build")
    p.add_argument("--rule-index")
    p.add_argument("--ir")
    p.add_argument("--out", required=True)
    p.add_argument("--cache-dir")
    p.add_argument("--run-id")
    p.add_argument("--snapshot-id")
    p.add_argument("--ir-digest")
    p.add_argument("--run-manifest")
    p.add_argument("--ir-manifest")
    p.add_argument("--strict", action="store_true")
    p.add_argument("--allow-partial", action="store_true")
    p.add_argument("--refresh", action="store_true")
    p.set_defaults(func=cmd_build)
    p = sub.add_parser("gate")
    p.add_argument("--registry", required=True)
    p.add_argument("--rule-index")
    p.add_argument("--strict", action="store_true")
    p.set_defaults(func=cmd_gate)
    return ap


def main() -> int:
    args = build_parser().parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
