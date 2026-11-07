from pathlib import Path

from scripts.size_gate import measure_roots


def test_measure_roots_keeps_active_and_archive_totals_separate(tmp_path: Path) -> None:
    database = tmp_path / "database"
    backup = tmp_path / "backup"
    database.mkdir()
    backup.mkdir()
    (database / "active.txt").write_bytes(b"a" * 1024)
    (backup / "snapshot.bin").write_bytes(b"b" * 4096)

    active_total, _ = measure_roots([database])
    archive_total, _ = measure_roots([backup])

    assert active_total == 1024
    assert archive_total == 4096
    assert active_total + archive_total == 5120
