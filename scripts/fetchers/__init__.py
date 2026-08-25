"""Source fetchers: GitHubRaw, CDN, HTTP."""
from .base import FetchResult, BaseFetcher
from .github_raw import GitHubRawFetcher
from .cdn import CDNFetcher
from .http_fetcher import HTTPFetcher


def get_fetcher(fetch_cfg: dict) -> BaseFetcher:
    t = (fetch_cfg or {}).get("type", "github_raw")
    if t == "github_raw":
        return GitHubRawFetcher(fetch_cfg)
    if t == "cdn":
        return CDNFetcher(fetch_cfg)
    if t in ("http", "url"):
        return HTTPFetcher(fetch_cfg)
    raise ValueError(f"unknown fetcher type: {t}")


__all__ = [
    "FetchResult",
    "BaseFetcher",
    "GitHubRawFetcher",
    "CDNFetcher",
    "HTTPFetcher",
    "get_fetcher",
]
