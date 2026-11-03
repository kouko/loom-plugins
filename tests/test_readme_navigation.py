"""Readers can navigate the project, plugin and skill documentation."""

from pathlib import Path
import re

import pytest


ROOT = Path(__file__).resolve().parents[1]
PLUGINS = ("loom-code", "loom-design", "loom-workflow")
REPOSITORY_FILES = "https://github.com/kouko/loom-plugins/blob/main/"


def local_targets(page: Path) -> set[Path]:
    """Resolve prose links into the checkout, including canonical GitHub links."""
    targets = set()
    prose = re.sub(r"<!--.*?-->", "", page.read_text(), flags=re.S)
    prose = re.sub(
        r"(?ms)^ {0,3}(`{3,}|~{3,})[^\n]*\n.*?^ {0,3}\1[ \t]*(?:\n|$)",
        "", prose,
    )
    for link in re.findall(r"\[[^\]]*\]\(([^)]+)\)", prose):
        target = link.split("#", 1)[0]
        if target.startswith(REPOSITORY_FILES):
            targets.add((ROOT / target.removeprefix(REPOSITORY_FILES)).resolve())
        elif target and not re.match(r"[a-z]+:", target):
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
        assert (skill.parent / "README.md").is_file(), skill.parent
        for page in skill.parent.glob("README*.md"):
            targets = local_targets(page)
            assert ROOT / "README.md" in targets, page
            assert any(
                target.parent == ROOT / plugin and target.name.startswith("README")
                for target in targets
            ), page
            assert skill in targets, page


@pytest.mark.parametrize("plugin", PLUGINS)
def test_documentation_navigation_has_no_missing_local_destinations(plugin):
    directory = ROOT / plugin
    pages = list(directory.glob("README*.md"))
    pages.extend(directory.glob("skills/*/README*.md"))
    for page in [ROOT / "README.md", *pages]:
        for target in local_targets(page):
            assert target.exists(), (page, target)
