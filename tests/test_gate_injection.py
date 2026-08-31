import subprocess
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]


def test_gate_injection():
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "gate_failure_injection.py")], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
