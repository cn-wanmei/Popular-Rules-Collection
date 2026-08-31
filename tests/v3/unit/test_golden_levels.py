from pathlib import Path
from src.v3.golden.runner import run_golden

def test_golden_runs():
    root = Path(__file__).resolve().parents[3]
    report = run_golden(root)
    assert "results" in report
    assert len(report["results"]) == 7
