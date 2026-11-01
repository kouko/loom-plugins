# concern: Parentheses in Markdown link targets can hide malformed diagrams from validation.
"""Check that a linked diagram with parentheses in its name is validated."""

import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[2] / "skills/loom-interactive-diagram/scripts/diagram.py"


def test_parenthesized_malformed_rejected(tmp_path):
    """An inline link with a parenthesized file name must be checked."""
    (tmp_path / "spec.md").write_text("See [diagram](hidden/broken(test).drawio).\n")
    hidden = tmp_path / "hidden"
    hidden.mkdir()
    (hidden / "broken(test).drawio").write_text("<broken")
    checked = subprocess.run([sys.executable, str(SCRIPT), "check"], cwd=tmp_path, capture_output=True, text=True)
    assert checked.returncode != 0
    assert "broken(test).drawio" in checked.stderr
