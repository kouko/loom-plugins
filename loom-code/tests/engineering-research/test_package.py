# concern: source-policy guidance can become unreachable or nonportable when bundled references drift.
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
    "references/preservation.md",
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


def test_code_owns_the_only_discoverable_package_without_design_routing():
    root = Path(__file__).resolve().parents[3]
    assert PACKAGE == root / "loom-code/skills/engineering-research"
    assert not (root / "loom-workflow/skills/engineering-research").exists()
    for path in (root / "loom-design/skills").rglob("*.md"):
        assert "engineering-research" not in path.read_text(), path
    code_router = (root / "loom-code/skills/using-loom-code/SKILL.md").read_text()
    assert "[engineering-research](../engineering-research/SKILL.md)" in code_router
    workflow_router = root / "loom-workflow/skills/using-loom-workflow/SKILL.md"
    assert "engineering-research" not in workflow_router.read_text()


def test_code_stations_delegate_research_to_their_bundled_skill():
    root = Path(__file__).resolve().parents[3]
    for station in ("write-plan", "build", "ship"):
        text = (root / f"loom-code/skills/{station}/SKILL.md").read_text()
        calls = set(re.findall(r"`(loom-[\w-]+:engineering-research)`", text))
        assert calls == {"loom-code:engineering-research"}, station
