"""Readers can navigate the project, plugin and skill documentation."""

from pathlib import Path
import re

import pytest


ROOT = Path(__file__).resolve().parents[1]
PLUGINS = ("loom-code", "loom-design", "loom-workflow")


def local_targets(page: Path) -> set[Path]:
    targets = set()
    for link in re.findall(r"\[[^\]]*\]\(([^)]+)\)", page.read_text()):
        target = link.split("#", 1)[0]
        if target and not re.match(r"[a-z]+:", target):
            targets.add((page.parent / target).resolve())
    return targets


@pytest.mark.parametrize("plugin", PLUGINS)
def test_all_skills_have_readmes_reachable_from_each_catalog(plugin):
    directory = ROOT / plugin
    skill_pages = {
        skill.parent / "README.md"
        for skill in (directory / "skills").glob("*/SKILL.md")
    }
    assert skill_pages
    assert all(page.is_file() for page in skill_pages), sorted(
        str(page.relative_to(ROOT)) for page in skill_pages if not page.is_file()
    )
    assert directory / "README.md" in local_targets(ROOT / "README.md")
    assert skill_pages <= local_targets(ROOT / "README.md")
    for catalog in directory.glob("README*.md"):
        targets = local_targets(catalog)
        # Localized skill pages may be linked instead of the English page.
        assert all(
            any(target.parent == page.parent and target.name.startswith("README")
                for target in targets)
            for page in skill_pages
        ), catalog
        assert ROOT / "README.md" in targets, catalog


@pytest.mark.parametrize("plugin", PLUGINS)
def test_skill_pages_link_back_up_and_to_runtime_instructions(plugin):
    for skill in (ROOT / plugin / "skills").glob("*/SKILL.md"):
        page = skill.parent / "README.md"
        assert page.is_file(), page
        targets = local_targets(page)
        assert ROOT / "README.md" in targets, page
        assert ROOT / plugin / "README.md" in targets, page
        assert skill in targets, page


@pytest.mark.parametrize("plugin", PLUGINS)
def test_documentation_navigation_has_no_missing_local_destinations(plugin):
    directory = ROOT / plugin
    pages = list(directory.glob("README*.md"))
    pages.extend(directory.glob("skills/*/README*.md"))
    for page in [ROOT / "README.md", *pages]:
        for target in local_targets(page):
            assert target.exists(), (page, target)
