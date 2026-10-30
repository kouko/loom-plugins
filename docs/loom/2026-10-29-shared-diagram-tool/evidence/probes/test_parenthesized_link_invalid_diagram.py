# concern: Parentheses in Markdown link targets can hide malformed diagrams from validation.
"""Check that a linked diagram with parentheses in its name is validated."""

import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[5] / "loom-workflow/skills/loom-interactive-diagram/scripts/diagram.py"


def test_parenthesized_malformed_rejected(tmp_path):
    """An inline link with a parenthesized file name must be checked."""
    (tmp_path / "spec.md").write_text("See [diagram](hidden/broken(test).drawio).\n")
    hidden = tmp_path / "hidden"
    hidden.mkdir()
    (hidden / "broken(test).drawio").write_text("<broken")
    created = subprocess.run([sys.executable, str(SCRIPT), "new", "valid"], cwd=tmp_path, capture_output=True, text=True)
    assert created.returncode == 0, created.stderr

    checked = subprocess.run([sys.executable, str(SCRIPT), "check"], cwd=tmp_path, capture_output=True, text=True)
    assert checked.returncode != 0
    assert "broken(test).drawio" in checked.stderr
