# concern: standalone output directory symlinks can redirect writes outside the selected project
"""Refuse a project destination whose apparent path redirects elsewhere."""

import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[2] / "skills/loom-interactive-diagram/scripts/diagram.py"


def run(cwd, *args):
    return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], cwd=cwd, text=True, capture_output=True)


def test_destination_symlink_rejected(tmp_path):
    """A named project alias must not create files in its unseen target."""
    root = tmp_path.resolve()
    outside = root / "outside"
    outside.mkdir()
    alias = root / "project"
    alias.symlink_to(outside, target_is_directory=True)

    result = run(root, "new", "redirected", "--output-dir", alias)

    assert result.returncode != 0
    assert not (outside / "redirected.drawio").exists()
    assert not (outside / "redirected.projection.md").exists()
