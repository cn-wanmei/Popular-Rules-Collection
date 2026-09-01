"""Small filesystem CAS: sha256 addressed immutable blobs."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def put_bytes(data: bytes, root: Path) -> str:
    root = Path(root)
    digest = digest_bytes(data)
    target = root / digest[:2] / digest[2:]
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        tmp = target.with_name(f".{target.name}.tmp-{os.getpid()}")
        tmp.write_bytes(data)
        tmp.replace(target)
    return digest


def put_file(path: Path, root: Path) -> str:
    return put_bytes(Path(path).read_bytes(), root)


def has(digest: str, root: Path) -> bool:
    digest = digest.lower()
    return (Path(root) / digest[:2] / digest[2:]).is_file()


def read_bytes(digest: str, root: Path) -> bytes:
    digest = digest.lower()
    path = Path(root) / digest[:2] / digest[2:]
    if not path.is_file():
        raise FileNotFoundError(f"CAS object not found: {digest}")
    data = path.read_bytes()
    if digest_bytes(data) != digest:
        raise RuntimeError(f"CAS digest mismatch: {digest}")
    return data
