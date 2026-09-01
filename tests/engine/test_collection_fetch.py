from __future__ import annotations

import hashlib
from pathlib import Path
from unittest.mock import patch

from src.engine.collection.source_state import FetchStateStore
from scripts.collect import _fetch_entry, collect_source
from scripts.fetchers.base import FetchResult


def test_304_reuses_verified_local_cache(tmp_path: Path) -> None:
    cached = tmp_path / "backup" / "2026-09-02" / "sources" / "demo" / "apple.yaml"
    cached.parent.mkdir(parents=True)
    content = b"payload\n"
    cached.write_bytes(content)

    previous = {
        "etag": '"abc"',
        "sha256": hashlib.sha256(content).hexdigest(),
        "size": len(content),
        "local": "backup/2026-09-02/sources/demo/apple.yaml",
    }
    result = FetchResult(
        ok=True, source_id="demo", path="rule/apple.yaml", name="apple.yaml",
        url="https://example.invalid/apple.yaml", status_code=304,
        not_modified=True, headers={"etag": '"abc"'},
    )
    with patch("scripts.collect.ROOT", tmp_path), patch("scripts.collect.get_fetcher") as get_fetcher:
        get_fetcher.return_value.fetch_one.return_value = result
        out = _fetch_entry("demo", {"type": "http"}, {
            "path": "rule/apple.yaml", "name": "apple.yaml", "service": "apple"
        }, previous)
    assert out["status"] == "not_modified"
    assert out["sha256"] == previous["sha256"]
    assert out["content"] == content


def test_304_with_corrupt_cache_refetches_without_validators(tmp_path: Path) -> None:
    cached = tmp_path / "backup" / "old" / "demo.txt"
    cached.parent.mkdir(parents=True)
    cached.write_bytes(b"corrupt")
    good = b"fresh\n"
    previous = {"etag": '"abc"', "sha256": hashlib.sha256(b"expected\n").hexdigest(), "local": "backup/old/demo.txt"}
    first = FetchResult(ok=True, source_id="", path="x", name="demo.txt", url="u", status_code=304, not_modified=True, headers={})
    second = FetchResult(ok=True, source_id="", path="x", name="demo.txt", url="u", content=good, status_code=200, headers={})
    second.compute_hash()
    with patch("scripts.collect.ROOT", tmp_path), patch("scripts.collect.get_fetcher") as get_fetcher:
        get_fetcher.return_value.fetch_one.side_effect = [first, second]
        out = _fetch_entry("demo", {"type": "http"}, {"path": "x", "name": "demo.txt", "service": "demo"}, previous)
    assert out["status"] == "ok"
    assert out["sha256"] == hashlib.sha256(good).hexdigest()


def test_collect_source_stably_sorts_concurrent_results_and_persists_relative_cache_path(tmp_path: Path) -> None:
    day_dir = tmp_path / "backup" / "2026-09-02"
    health: dict = {}
    state = FetchStateStore(tmp_path / "state.json")
    src = {"id": "demo", "fetch": {"type": "http"}, "rules": [
        {"path": "b", "name": "b.txt", "service": "b"},
        {"path": "a", "name": "a.txt", "service": "a"},
    ]}
    results = {
        "a": FetchResult(True, "", "a", "a.txt", "u", content=b"a\n", status_code=200),
        "b": FetchResult(True, "", "b", "b.txt", "u", content=b"b\n", status_code=200),
    }
    for r in results.values():
        r.compute_hash()

    class FakeFetcher:
        def fetch_one(self, entry):
            return results[entry["name"].split(".")[0]]

    with patch("scripts.collect.get_fetcher", return_value=FakeFetcher()), patch("scripts.collect.ROOT", tmp_path):
        report = collect_source(src, day_dir, health, state, 2)
    assert [x["name"] for x in report["files"]] == ["a.txt", "b.txt"]
    assert report["concurrency_workers"] == 2
    assert report["files_ok"] == 2
    assert state.get("demo::a")["local"] == "backup/2026-09-02/sources/demo/a.txt"
    assert state.get("demo::b")["local"] == "backup/2026-09-02/sources/demo/b.txt"
