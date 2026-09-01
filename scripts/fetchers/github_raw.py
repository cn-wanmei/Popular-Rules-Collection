from __future__ import annotations

from urllib.parse import quote

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .base import BaseFetcher, FetchResult

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "Popular-Rules-Collection/1.3"})
SESSION.mount(
    "https://",
    HTTPAdapter(max_retries=Retry(
        total=3, connect=3, read=3, backoff_factor=0.6,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET", "HEAD"}),
        respect_retry_after_header=True,
    )),
)


def _encode_path(path: str) -> str:
    """Encode each path segment (spaces, unicode) for raw.githubusercontent.com."""
    return "/".join(quote(seg, safe="") for seg in path.split("/"))


class GitHubRawFetcher(BaseFetcher):
    def fetch_one(self, entry: dict[str, str]) -> FetchResult:
        owner = self.cfg["owner"]
        repo = self.cfg["repo"]
        branch = self.cfg.get("branch", "master")
        path = entry["path"]
        name = entry.get("name") or path.replace("/", "_")
        url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{_encode_path(path)}"
        try:
            r = SESSION.get(url, headers=self.request_headers(entry), timeout=(15, 90))
            headers = {k.lower(): v for k, v in r.headers.items()}
            if r.status_code == 304:
                return FetchResult(
                    ok=True, source_id="", path=path, name=name, url=url,
                    status_code=304, not_modified=True, headers=headers,
                )
            if r.status_code != 200:
                return FetchResult(
                    ok=False, source_id="", path=path, name=name, url=url,
                    error=f"HTTP {r.status_code}", status_code=r.status_code,
                    headers=headers,
                )
            fr = FetchResult(
                ok=True, source_id="", path=path, name=name, url=url,
                content=r.content, status_code=200, headers=headers,
            )
            fr.compute_hash()
            return fr
        except requests.RequestException as e:
            return FetchResult(
                ok=False, source_id="", path=path, name=name, url=url, error=str(e),
            )
