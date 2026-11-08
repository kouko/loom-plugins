"""Portable package invariants, not proof of research-agent behavior."""

from pathlib import Path
import re

import yaml


PACKAGE = Path(__file__).resolve().parents[2] / "skills" / "engineering-research"
RESOURCES = {
    "references/research-methods.md",
    "references/source-policy.md",
    "references/evaluation-selection.md",
    "references/structured-relations.md",
    "templates/research.md",
}


def test_bundled_resources_are_flat_and_all_links_resolve():
    entry = PACKAGE / "SKILL.md"
    assert entry.is_file()
    for resource in RESOURCES:
        assert (PACKAGE / resource).is_file(), resource
    for path in PACKAGE.rglob("*"):
        if path.is_file():
            assert len(path.relative_to(PACKAGE).parts) <= 2, path
            text = path.read_text()
            assert "/Users/" not in text
            for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
                if "://" not in target and not target.startswith("#"):
                    assert (path.parent / target.split("#")[0]).is_file(), target


def test_research_template_has_flat_portable_metadata():
    text = (PACKAGE / "templates/research.md").read_text()
    metadata = yaml.safe_load(text.split("---", 2)[1])
    assert set(metadata) == {"title", "type", "status", "created", "updated", "tags"}
    assert metadata["type"] == "loom-research"
    assert metadata["status"] in {"in-progress", "concluded", "superseded"}
    assert metadata["tags"] == ["loom/research"]
    assert metadata["created"] == metadata["updated"] == "YYYY-MM-DD"
    assert all(not isinstance(value, dict) for value in metadata.values())


def test_entry_routes_every_core_resource_directly():
    text = (PACKAGE / "SKILL.md").read_text()
    targets = set(re.findall(r"\[[^\]]*\]\(([^)]+)\)", text))
    assert RESOURCES <= targets
    metadata = yaml.safe_load(text.split("---", 2)[1])
    assert metadata["name"] == PACKAGE.name
    assert isinstance(metadata["description"], str)
    assert len(metadata["description"]) <= 250
