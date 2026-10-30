# concern: Reference-style Markdown links can hide malformed diagrams from validation.
"""Check that a spec reference to a malformed diagram fails validation."""

import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[2] / "skills/loom-interactive-diagram/scripts/diagram.py"


def test_reference_malformed_rejected(tmp_path):
    """A reference-style link to an invalid diagram must be checked."""
    (tmp_path / "spec.md").write_text("See [diagram][flow].\n\n[flow]: hidden/broken.drawio\n")
    hidden = tmp_path / "hidden"
    hidden.mkdir()
    (hidden / "broken.drawio").write_text("<broken")
    created = subprocess.run([sys.executable, str(SCRIPT), "new", "valid"], cwd=tmp_path, capture_output=True, text=True)
    assert created.returncode == 0, created.stderr

    checked = subprocess.run([sys.executable, str(SCRIPT), "check"], cwd=tmp_path, capture_output=True, text=True)
    assert checked.returncode != 0
    assert "broken.drawio" in checked.stderr
