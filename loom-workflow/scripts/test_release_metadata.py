"""loom-workflow version pins stay in step with each other.

The installer only refetches a plugin when its version changes, so a content
change shipped under a stale or split version never reaches installed copies.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
PLUGIN = REPO / "loom-workflow"
CURRENT = "5.3.2"


@pytest.mark.parametrize(
    "manifest",
    ["plugin.json", ".claude-plugin/plugin.json", ".codex-plugin/plugin.json"],
)
def test_manifest_version_is_current(manifest: str) -> None:
    data = json.loads((PLUGIN / manifest).read_text(encoding="utf-8"))
    assert data["version"] == CURRENT


def test_changelog_has_current_entry() -> None:
    changelog = (PLUGIN / "CHANGELOG.md").read_text(encoding="utf-8")
    assert f"## [{CURRENT}]" in changelog


@pytest.mark.parametrize("readme", ["README.md", "README.ja.md", "README.zh-TW.md"])
def test_plugin_readme_version_is_current(readme: str) -> None:
    text = (PLUGIN / readme).read_text(encoding="utf-8")
    match = re.search(r"^\*\*Version\*\*[:：]\s*(\d+\.\d+\.\d+)", text, re.M)
    assert match, f"{readme}: version line missing"
    assert match.group(1) == CURRENT


def test_root_readme_table_row_is_current() -> None:
    text = (REPO / "README.md").read_text(encoding="utf-8")
    row = re.search(
        r"^\| \[`loom-workflow`\]\(loom-workflow/\) \| (\d+\.\d+\.\d+) \|", text, re.M
    )
    assert row, "README.md: loom-workflow plugin table row missing"
    assert row.group(1) == CURRENT
