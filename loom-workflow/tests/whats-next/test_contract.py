from pathlib import Path
import re


WORKFLOW = Path(__file__).resolve().parents[2]
SKILL = WORKFLOW / "skills" / "whats-next" / "SKILL.md"


def test_skill_is_discoverable_and_self_contained():
    text = SKILL.read_text()
    assert re.search(r"^name: whats-next$", text, re.M)
    assert re.search(r"^user-invocable: true$", text, re.M)
    router = (WORKFLOW / "skills/using-loom-workflow/SKILL.md").read_text()
    assert "[whats-next](../whats-next/SKILL.md)" in router
    assert not list(SKILL.parent.glob("*/**/*"))
    for target in re.findall(r"\]\(([^)]+)\)", text):
        if not target.startswith("https://"):
            assert (SKILL.parent / target).exists()


def test_planning_owner_is_linked_from_advice_and_router():
    """Routing edges only; document ownership behavior needs semantic trials."""
    route = "../roadmap/SKILL.md"
    for source in (SKILL, WORKFLOW / "skills/using-loom-workflow/SKILL.md"):
        targets = re.findall(r"\]\(([^)]+)\)", source.read_text())
        assert route in targets, source
        assert (source.parent / route).is_file()
    router = (WORKFLOW / "skills/using-loom-workflow/SKILL.md").read_text()
    targets = re.findall(r"\]\(([^)]+)\)", router)
    assert "../decision-map/SKILL.md" not in targets
