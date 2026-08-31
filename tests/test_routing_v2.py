import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_routing_contract_validate():
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "routing_contract_validate.py")], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr


def test_routing_resolve_demo():
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "routing_resolve.py"), "--demo"], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
