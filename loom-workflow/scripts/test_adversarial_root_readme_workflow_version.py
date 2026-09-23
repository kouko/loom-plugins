"""Adversarial probe: the root README's loom-workflow section states a stale version.

concern: a release bump that updates the plugin manifests and the README table
but leaves a second version pin in the same README, so the published overview
tells readers two different versions of one plugin.

This change bumps loom-workflow to the version its three manifests carry. The
root README states that version twice: once in the plugin table (pinned by
`loom-workflow/scripts/test_release_metadata.py`) and once as the first line of
its `## loom-workflow` section, which no test reads. The loom-code section's
line has its own pin in `test_write_plan_station_text.py`; the loom-workflow
one has none, and the bump left it behind.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _section(text: str, heading: str) -> str:
    start = text.index(heading + "\n")
    rest = text[start + len(heading) + 1:]
    end = rest.find("\n## ")
    return rest if end == -1 else rest[:end]


def test_root_readme_workflow_section_version_matches_manifest() -> None:
    """The `## loom-workflow` section's `Version X.Y.Z.` line equals the manifest version."""
    manifest = json.loads((ROOT / "loom-workflow/plugin.json").read_text(encoding="utf-8"))
    section = _section((ROOT / "README.md").read_text(encoding="utf-8"), "## loom-workflow")
    match = re.search(r"^Version (\d+\.\d+\.\d+)\.", section, re.MULTILINE)
    assert match, "README.md ## loom-workflow: version line missing"
    assert match.group(1) == manifest["version"]
