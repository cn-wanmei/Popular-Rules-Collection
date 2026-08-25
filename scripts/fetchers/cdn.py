from __future__ import annotations

import requests
from .base import BaseFetcher, FetchResult

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "Popular-Rules-Collection/1.1"})


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
                r = SESSION.get(url, timeout=90)
                if r.status_code == 200 and r.content:
                    fr = FetchResult(
                        ok=True, source_id="", path=path, name=name, url=url,
                        content=r.content, status_code=200,
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
