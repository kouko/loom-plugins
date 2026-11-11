"""Portable discovery and resource invariants; behavior is tested independently."""

from pathlib import Path
import re

import yaml


ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "loom-design/skills/design-research"


def test_design_research_is_discoverable_and_self_contained():
    entry = PACKAGE / "SKILL.md"
    metadata = yaml.safe_load(entry.read_text().split("---", 2)[1])
    assert metadata["name"] == PACKAGE.name
    assert 0 < len(metadata["description"]) <= 250
    router = ROOT / "loom-design/skills/using-loom-design/SKILL.md"
    assert "[design-research](../design-research/SKILL.md)" in router.read_text()
    manifest = yaml.safe_load((ROOT / "loom-code/contract/manifest.yaml").read_text())
    tool = next(t for t in manifest["tools"] if t["name"] == PACKAGE.name)
    assert tool == {"name": "design-research", "owner": "loom-design"}
    for path in PACKAGE.rglob("*.md"):
        assert len(path.relative_to(PACKAGE).parts) <= 2
        text = path.read_text()
        assert "/Users/" not in text
        assert "loom-code/" not in text
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
            if "://" not in target and not target.startswith("#"):
                resolved = (path.parent / target.split("#")[0]).resolve()
                assert resolved.is_relative_to(PACKAGE.resolve())
                assert resolved.is_file()


def test_design_research_template_keeps_flat_portable_metadata():
    template = PACKAGE / "templates/research.md"
    data = yaml.safe_load(template.read_text().split("---", 2)[1])
    assert set(data) == {"title", "type", "status", "created", "updated", "tags"}
    assert data["type"] == "loom-research"
    assert data["status"] in {"in-progress", "concluded", "superseded"}
    assert data["created"] == data["updated"] == "YYYY-MM-DD"
    assert data["tags"] == ["loom/research"]
    assert all(not isinstance(value, dict) for value in data.values())
