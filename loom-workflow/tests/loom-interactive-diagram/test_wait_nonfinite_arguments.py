# concern: Non-finite wait arguments can end an active turn immediately or leave it waiting forever.
"""Reject non-finite durations before the diagram wait begins."""

import subprocess
import sys
from pathlib import Path

import pytest


SCRIPT = Path(__file__).resolve().parents[2] / "skills/loom-interactive-diagram/scripts/wait_for_save.py"


@pytest.mark.parametrize("option,value", [
    ("--timeout", "nan"),
    ("--timeout", "inf"),
    ("--interval", "nan"),
    ("--interval", "inf"),
])
def test_wait_nonfinite_rejected(tmp_path, option, value):
    """A bounded wait refuses durations that are not finite numbers."""
    diagram = tmp_path / "flow.drawio"
    diagram.write_text("baseline")
    try:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(diagram), option, value],
            text=True,
            capture_output=True,
            timeout=0.5,
        )
    except subprocess.TimeoutExpired:
        pytest.fail(f"{option}={value} left the waiter running")
    assert result.returncode != 0
    assert "READY" not in result.stdout
    assert "error:" in result.stderr.lower()
