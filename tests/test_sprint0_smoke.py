import os
import shutil
import subprocess
import sys
from pathlib import Path


def test_demo_runs_successfully(tmp_path):
    temp_memory_path = tmp_path / "application_health_memory.json"
    temp_history_path = tmp_path / "execution_history.json"

    shutil.copy(
        Path("data/memory/application_health_memory.json"),
        temp_memory_path,
    )
    temp_history_path.write_text("[]", encoding="utf-8")

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["EAIOS_MEMORY_PATH"] = str(temp_memory_path)
    env["EAIOS_EXECUTION_HISTORY_PATH"] = str(temp_history_path)

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