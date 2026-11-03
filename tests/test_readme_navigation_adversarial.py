"""Exercise navigation checks against regressions hidden by valid English pages."""

# concern: localized guides losing their navigation while English-only checks pass
import importlib.util
from pathlib import Path
import shutil

import pytest


ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def navigation(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location(
        "navigation_under_attack", ROOT / "tests/test_readme_navigation.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for plugin in module.PLUGINS:
        for source in (ROOT / plugin).glob("skills/*/*"):
            if source.is_file() and (
                source.name == "SKILL.md" or source.name.startswith("README")
            ):
                target = tmp_path / source.relative_to(ROOT)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
    monkeypatch.setattr(module, "ROOT", tmp_path)
    return module


@pytest.mark.parametrize("language", ["ja", "zh-TW"])
@pytest.mark.parametrize(
    "destination", [
        "https://github.com/kouko/loom-plugins/blob/main/README.md",
        "../../README.{language}.md",
        "SKILL.md",
    ]
)
def test_backlinks_localized_rejectmissing(navigation, language, destination):
    """Reject a translated guide that loses one required navigation link."""
    check = navigation.test_skill_pages_link_back_up_and_to_runtime_instructions
    check("loom-workflow")
    page = navigation.ROOT / f"loom-workflow/skills/handoff/README.{language}.md"
    destination = destination.format(language=language)
    before = page.read_text()
    needle = f"]({destination})"
    assert needle in before
    page.write_text(before.replace(needle, "](#removed-navigation)"))
    with pytest.raises(AssertionError):
        check("loom-workflow")


@pytest.mark.parametrize("wrapper", ["<!-- {} -->", "```markdown\n{}\n```"])
def test_links_nonrendered_ignoretargets(tmp_path, wrapper):
    """Do not treat comments or fenced examples as clickable navigation."""
    spec = importlib.util.spec_from_file_location(
        "navigation_parser_under_attack", ROOT / "tests/test_readme_navigation.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    page = tmp_path / "README.md"
    page.write_text("[Visible](visible.md)\n" + wrapper.format("[Hidden](hidden.md)"))
    assert module.local_targets(page) == {tmp_path / "visible.md"}
