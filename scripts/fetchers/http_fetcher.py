from __future__ import annotations

import requests
from .base import BaseFetcher, FetchResult

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "Popular-Rules-Collection/1.1"})


class HTTPFetcher(BaseFetcher):
    def fetch_one(self, entry: dict[str, str]) -> FetchResult:
        url = entry.get("url") or entry["path"]
        name = entry.get("name") or url.split("/")[-1]
        try:
            r = SESSION.get(url, timeout=90)
            if r.status_code != 200:
                return FetchResult(
                    ok=False, source_id="", path=url, name=name, url=url,
                    error=f"HTTP {r.status_code}", status_code=r.status_code,
                )
            fr = FetchResult(
                ok=True, source_id="", path=url, name=name, url=url,
                content=r.content, status_code=200,
            )
            fr.compute_hash()
            return fr
        except requests.RequestException as e:
            return FetchResult(
                ok=False, source_id="", path=url, name=name, url=url, error=str(e),
            )
