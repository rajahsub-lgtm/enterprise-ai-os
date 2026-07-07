import os
import subprocess
import sys


def test_demo_runs_successfully():
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    result = subprocess.run(
        [sys.executable, "demo.py"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=20,
        env=env,
    )

    assert result.returncode == 0, result.stderr
    assert "EAIOS Demo: Application Health" in result.stdout
    assert "EAIOS ENTERPRISE ALERT" in result.stdout
    assert "Recommendation Agent" in result.stdout
    assert "Human Approval Required" in result.stdout