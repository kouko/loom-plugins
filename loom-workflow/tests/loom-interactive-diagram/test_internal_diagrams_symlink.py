# concern: an internal diagrams symlink redirects generated artifacts outside diagrams/
"""Adversarial coverage for the per-change diagram output boundary."""

import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[2] / "skills/loom-interactive-diagram/scripts/diagram.py"


def test_new_symlink_rejected(tmp_path):
    """A diagrams symlink to another change folder must not receive artifacts."""
    store = tmp_path / "docs/loom"
    intent = store / "intent"
    intent.mkdir(parents=True)
    (intent / "example.md").write_text("# Example\n", encoding="utf-8")
    change = store / "example"
    change.mkdir()
    diverted = change / "other"
    diverted.mkdir()
    (change / "diagrams").symlink_to(diverted, target_is_directory=True)

    result = subprocess.run(
        [sys.executable, str(SCRIPT), "new", "sample"],
        cwd=change,
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0, result.stdout
    assert list(diverted.iterdir()) == []
