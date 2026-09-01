from __future__ import annotations

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


def _encode_path(path: str) -> str:
    """Encode each path segment (spaces, unicode) for upstream URLs."""
    return "/".join(quote(seg, safe="") for seg in path.split("/"))


def _upstream_urls(cfg: dict, path: str) -> list[str]:
    """Return the configured GitHub Raw endpoint followed by a CDN fallback.

    The CDN fallback is only used after a transient transport/status failure;
    permanent upstream errors such as 404 are returned directly so bad registry
    paths are not masked.
    """
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


class GitHubRawFetcher(BaseFetcher):
    def fetch_one(self, entry: dict[str, str]) -> FetchResult:
        path = entry["path"]
        name = entry.get("name") or path.replace("/", "_")
        urls = _upstream_urls(self.cfg, path)
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
            except requests.RequestException as exc:
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
