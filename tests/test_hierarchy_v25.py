import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_hierarchy_v27():
    for script in ("hierarchy_validate.py", "resolve_hierarchy.py", "hierarchy_golden.py", "hierarchy_coverage.py"):
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / script)], cwd=ROOT, capture_output=True, text=True, timeout=120)
        assert r.returncode == 0, script + "\n" + r.stdout + r.stderr
