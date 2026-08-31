import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_build_and_golden():
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "build_mihomo_ir.py")], cwd=ROOT, capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, r.stdout + r.stderr
    r2 = subprocess.run([sys.executable, str(ROOT / "scripts" / "mihomo_ir_golden.py")], cwd=ROOT, capture_output=True, text=True, timeout=60)
    assert r2.returncode == 0, r2.stdout + r2.stderr
