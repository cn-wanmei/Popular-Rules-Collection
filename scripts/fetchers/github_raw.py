from __future__ import annotations

import hashlib
import json
from pathlib import Path
from urllib.parse import quote

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .base import BaseFetcher, FetchResult

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "Popular-Rules-Collection/1.4"})
SESSION.mount(
    "https://",
    HTTPAdapter(max_retries=Retry(
        total=3, connect=3, read=3, backoff_factor=0.6,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET", "HEAD"}),
        respect_retry_after_header=True,
    )),
)

TRANSIENT_STATUS_CODES = frozenset({429, 500, 502, 503, 504})
ROOT = Path(__file__).resolve().parents[2]
IMMUTABLE_REGISTRY = ROOT / "sources" / "immutable_registry.yaml"


def _encode_path(path: str) -> str:
    """Encode each path segment (spaces, unicode) for upstream URLs."""
    return "/".join(quote(seg, safe="") for seg in path.split("/"))


def _upstream_urls(cfg: dict, path: str) -> list[str]:
    """Return the configured GitHub Raw endpoint followed by a CDN fallback."""
    owner = str(cfg["owner"])
    repo = str(cfg["repo"])
    branch = str(cfg.get("branch", "master"))
    encoded = _encode_path(path)
    raw = f"https://raw.githubusercontent.com/{owner}/{repo}/{quote(branch, safe='')}/{encoded}"
    configured = cfg.get("fallback_bases")
    if configured is None:
        bases = [f"https://cdn.jsdelivr.net/gh/{owner}/{repo}@{quote(branch, safe='')}"]
    else:
        bases = [str(base).rstrip("/") for base in configured if str(base).strip()]
    return [raw, *[f"{base}/{encoded}" for base in bases]]


def _load_immutable_binding(service: str) -> dict | None:
    if not IMMUTABLE_REGISTRY.exists():
        return None
    import yaml
    data = yaml.safe_load(IMMUTABLE_REGISTRY.read_text(encoding="utf-8")) or {}
    wanted = str(service).strip().casefold()
    binding = next(
        (value for key, value in (data.get("bindings") or {}).items()
         if str(key).strip().casefold() == wanted and isinstance(value, dict)),
        None,
    )
    return binding if isinstance(binding, dict) else None


def _immutable_cfg(entry: dict[str, str], cfg: dict) -> tuple[dict, str, dict | None]:
    service = str(entry.get("service") or "").lower()
    binding = _load_immutable_binding(service)
    if not binding:
        return cfg, entry["path"], None
    if binding.get("status") != "active":
        raise ValueError(f"immutable source binding for {service} is not active")
    ref = str(binding.get("source_ref") or "")
    if len(ref) != 40 or any(ch not in "0123456789abcdef" for ch in ref.lower()):
        raise ValueError(f"immutable source binding for {service} requires a 40-char commit SHA")
    source_id = str(binding.get("source_id") or "")
    if source_id != str(cfg.get("source_id") or "popular-rules-source"):
        raise ValueError(f"immutable source binding source mismatch for {service}")
    path = str(binding.get("artifact_path") or entry["path"])
    expected_sha256 = str(binding.get("expected_sha256") or "")
    release_path = str(binding.get("release_path") or "")
    snapshot_id = str(binding.get("snapshot_id") or "")
    content_digest = str(binding.get("content_digest") or "")
    if not expected_sha256 or not release_path or not snapshot_id or not content_digest:
        raise ValueError(f"immutable source binding for {service} is incomplete")
    resolved = {**cfg, "branch": ref, "fallback_bases": []}
    metadata = {
        "service": service,
        "release_path": release_path,
        "snapshot_id": snapshot_id,
        "content_digest": content_digest,
        "expected_sha256": expected_sha256,
    }
    return resolved, path, metadata


def _get_release(cfg: dict, release_path: str) -> dict:
    urls = _upstream_urls(cfg, release_path)
    r = SESSION.get(urls[0], timeout=(15, 60))
    if r.status_code != 200:
        raise ValueError(f"immutable release missing: HTTP {r.status_code} {release_path}")
    try:
        return r.json()
    except ValueError as exc:
        raise ValueError(f"immutable release is not JSON: {release_path}") from exc


class GitHubRawFetcher(BaseFetcher):
    def fetch_one(self, entry: dict[str, str]) -> FetchResult:
        path = entry["path"]
        name = entry.get("name") or path.replace("/", "_")
        try:
            cfg, path, immutable = _immutable_cfg(entry, self.cfg)
            if immutable:
                release = _get_release(cfg, immutable["release_path"])
                for key, expected in (("service_id", immutable["service"]), ("snapshot_id", immutable["snapshot_id"]), ("content_digest", immutable["content_digest"])):
                    if str(release.get(key)) != expected:
                        raise ValueError(f"immutable release identity mismatch for {immutable['service']}: {key}")
                required_files = set((release.get("checksums") or {}).keys())
                if "domains.txt" not in required_files:
                    raise ValueError(f"immutable release missing domains.txt checksum for {immutable['service']}")
        except ValueError as exc:
            return FetchResult(ok=False, source_id="", path=path, name=name, error=str(exc))

        urls = _upstream_urls(cfg, path)
        last_error: str | None = None
        last_status: int | None = None

        for index, url in enumerate(urls):
            try:
                r = SESSION.get(url, headers=self.request_headers(entry), timeout=(15, 90))
                headers = {k.lower(): v for k, v in r.headers.items()}
                if r.status_code == 304:
                    return FetchResult(
                        ok=True, source_id="", path=path, name=name, url=url,
                        status_code=304, not_modified=True, headers=headers,
                    )
                if r.status_code == 200:
                    if immutable:
                        actual = hashlib.sha256(r.content).hexdigest()
                        if actual != immutable["expected_sha256"]:
                            return FetchResult(
                                ok=False, source_id="", path=path, name=name, url=url,
                                error=f"immutable content digest mismatch: expected {immutable['expected_sha256']} got {actual}",
                                status_code=200, headers=headers,
                            )
                    fr = FetchResult(
                        ok=True, source_id="", path=path, name=name,
                        url=url, content=r.content, status_code=200, headers=headers,
                    )
                    fr.compute_hash()
                    return fr

                last_status = r.status_code
                last_error = f"HTTP {r.status_code}"
                if index == 0 and r.status_code in TRANSIENT_STATUS_CODES:
                    continue
                return FetchResult(
                    ok=False, source_id="", path=path, name=name, url=url,
                    error=last_error, status_code=last_status, headers=headers,
                )
            except (requests.RequestException, ValueError) as exc:
                last_error = str(exc)
                last_status = None
                if index + 1 < len(urls):
                    continue
                return FetchResult(
                    ok=False, source_id="", path=path, name=name, url=url,
                    error=last_error,
                )

        return FetchResult(
            ok=False, source_id="", path=path, name=name, url=urls[-1],
            error=last_error or "upstream fetch failed", status_code=last_status,
        )
