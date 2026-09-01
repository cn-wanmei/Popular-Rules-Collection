from pathlib import Path
from src.engine.validation.naming_gate import check_repo_layout

def test_no_v3_dirs():
    root = Path(__file__).resolve().parents[3]
    assert check_repo_layout(root) == []
