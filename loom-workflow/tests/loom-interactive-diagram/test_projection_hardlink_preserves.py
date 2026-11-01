# concern: in-place projection must not rewrite an unselected hard-linked file
"""Protect existing files that share an inode with a selected projection."""

import os
import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[2] / "skills/loom-interactive-diagram/scripts/diagram.py"


def run(cwd, *args):
    return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], cwd=cwd, text=True, capture_output=True)


def test_projection_hardlink_preserves(tmp_path):
    """Updating a projection must not alter another path to its inode."""
    root = tmp_path.resolve()
    project = root / "project"
    project.mkdir()
    created = run(root, "new", "source", "--output-dir", project)
    assert created.returncode == 0, created.stderr
    diagram = project / "source.drawio"
    projection = project / "source.projection.md"
    projection.unlink()
    protected = root / "unselected.md"
    protected.write_text("backend: drawio\n# Nodes\n- keep\n", encoding="utf-8")
    os.link(protected, projection)
    before = protected.read_bytes()

    result = run(root, "project", diagram, "--in-place")

    assert result.returncode == 0 or "hardlink" in result.stderr.lower()
    assert protected.read_bytes() == before
