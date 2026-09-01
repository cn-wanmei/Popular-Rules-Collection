from __future__ import annotations

import json
import os
from pathlib import Path

from src.engine.cas.gc import collect, referenced_digests
from src.engine.cas.store import put_bytes


def test_referenced_digests_reads_run_manifests(tmp_path: Path) -> None:
    run = tmp_path / "runs" / "r1"
    run.mkdir(parents=True)
    digest = "a" * 64
    (run / "cas-manifest.json").write_text(
        json.dumps({"objects": {"artifact.json": digest}}), encoding="utf-8"
    )
    assert referenced_digests([tmp_path / "runs"]) == {digest}


def test_collect_dry_run_protects_references_and_pins(tmp_path: Path) -> None:
    root = tmp_path / "cas"
    keep = put_bytes(b"keep", root)
    pin = put_bytes(b"pin", root)
    old = put_bytes(b"old", root)
    for digest in (keep, pin, old):
        path = root / digest[:2] / digest[2:]
        os.utime(path, (1, 1))

    result = collect(root, referenced=[keep], pinned=[pin], min_age_seconds=1, dry_run=True)
    assert result == {"scanned": 3, "eligible": 1, "deleted": 0}
    assert (root / old[:2] / old[2:]).is_file()


def test_collect_deletes_only_eligible_objects(tmp_path: Path) -> None:
    root = tmp_path / "cas"
    old = put_bytes(b"old", root)
    young = put_bytes(b"young", root)
    os.utime(root / old[:2] / old[2:], (1, 1))

    result = collect(root, min_age_seconds=1, dry_run=False)
    assert result == {"scanned": 2, "eligible": 1, "deleted": 1}
    assert not (root / old[:2] / old[2:]).exists()
    assert (root / young[:2] / young[2:]).exists()
