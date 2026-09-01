from __future__ import annotations

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .base import BaseFetcher, FetchResult

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "Popular-Rules-Collection/1.3"})
SESSION.mount(
    "http://", HTTPAdapter(max_retries=Retry(
        total=3, connect=3, read=3, backoff_factor=0.6,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET", "HEAD"}),
        respect_retry_after_header=True,
    )))
SESSION.mount(
    "https://", HTTPAdapter(max_retries=Retry(
        total=3, connect=3, read=3, backoff_factor=0.6,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET", "HEAD"}),
        respect_retry_after_header=True,
    )))


class CDNFetcher(BaseFetcher):
    def fetch_one(self, entry: dict[str, str]) -> FetchResult:
        bases = self.cfg.get("bases") or [self.cfg.get("base", "")]
        path = entry["path"]
        name = entry.get("name") or path.replace("/", "_")
        last_err = "no base"
        last_code = None
        for base in bases:
            base = base.rstrip("/")
            url = f"{base}/{path.lstrip('/')}"
            try:
                r = SESSION.get(url, headers=self.request_headers(entry), timeout=(15, 90))
                headers = {k.lower(): v for k, v in r.headers.items()}
                if r.status_code == 304:
                    return FetchResult(
                        ok=True, source_id="", path=path, name=name, url=url,
                        status_code=304, not_modified=True, headers=headers,
                    )
                if r.status_code == 200 and r.content:
                    fr = FetchResult(
                        ok=True, source_id="", path=path, name=name, url=url,
                        content=r.content, status_code=200, headers=headers,
                    )
                    fr.compute_hash()
                    return fr
                last_err = f"HTTP {r.status_code}"
                last_code = r.status_code
            except requests.RequestException as e:
                last_err = str(e)
        return FetchResult(
            ok=False, source_id="", path=path, name=name,
            url=f"{bases[0]}/{path}" if bases else path,
            error=last_err, status_code=last_code,
        )
