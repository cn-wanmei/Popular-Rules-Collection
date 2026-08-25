from __future__ import annotations

import requests
from .base import BaseFetcher, FetchResult

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "Popular-Rules-Collection/1.1"})


class GitHubRawFetcher(BaseFetcher):
    def fetch_one(self, entry: dict[str, str]) -> FetchResult:
        owner = self.cfg["owner"]
        repo = self.cfg["repo"]
        branch = self.cfg.get("branch", "master")
        path = entry["path"]
        name = entry.get("name") or path.replace("/", "_")
        url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"
        try:
            r = SESSION.get(url, timeout=90)
            if r.status_code != 200:
                return FetchResult(
                    ok=False, source_id="", path=path, name=name, url=url,
                    error=f"HTTP {r.status_code}", status_code=r.status_code,
                )
            fr = FetchResult(
                ok=True, source_id="", path=path, name=name, url=url,
                content=r.content, status_code=200,
            )
            fr.compute_hash()
            return fr
        except requests.RequestException as e:
            return FetchResult(
                ok=False, source_id="", path=path, name=name, url=url, error=str(e),
            )
