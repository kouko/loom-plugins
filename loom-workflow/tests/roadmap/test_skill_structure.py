"""Packaging checks only; semantic behavior is evaluated with independent runs."""

from pathlib import Path
import re


SKILL = Path(__file__).resolve().parents[2] / "skills" / "roadmap"


def test_independent_skill_identity_and_instruction_only_layout():
    text = (SKILL / "SKILL.md").read_text()
    frontmatter = text.split("---", 2)[1]
    assert re.search(r"^name: roadmap$", frontmatter, re.MULTILINE)
    assert re.search(r"^description: .+", frontmatter, re.MULTILINE)
    assert re.search(r"^user-invocable: true$", frontmatter, re.MULTILINE)
    assert {p.name for p in SKILL.iterdir()} == {"SKILL.md", "README.md"}


def test_packaged_markdown_local_links_resolve():
    for source in (SKILL / "SKILL.md", SKILL / "README.md"):
        assert source.is_file()
        for target in re.findall(r"\]\(([^)]+)\)", source.read_text()):
            if "://" not in target and not target.startswith("#"):
                assert (source.parent / target.split("#", 1)[0]).exists(), (source, target)
