"""CAS bridge for upstream acquisition.

Collection owns a repository-local CAS namespace while reusing the V3
filesystem CAS implementation. Acquisition never treats a mutable snapshot
path as the canonical cached object.
"""
from __future__ import annotations

from pathlib import Path

from src.engine.cas.store import digest_bytes, put_bytes, read_bytes


DEFAULT_ROOT = Path("data/cas/acquisition")


def object_root(repo_root: Path) -> Path:
    return Path(repo_root) / DEFAULT_ROOT


def store(data: bytes, repo_root: Path) -> str:
    return put_bytes(data, object_root(repo_root))


def load(digest: str, repo_root: Path) -> bytes:
    return read_bytes(digest, object_root(repo_root))


def verify(data: bytes, digest: str) -> bool:
    return digest_bytes(data) == digest
