"""The single-session retrospective proposes project changes for later work."""

from pathlib import Path


SKILL = Path(__file__).resolve().parents[2] / "skills" / "project-retro" / "SKILL.md"


def skill_text() -> str:
    return SKILL.read_text(encoding="utf-8")


def test_project_surface_and_source_linked_handoff() -> None:
    text = skill_text()
    assert "name: project-retro" in text
    assert "one coding session" in text
    assert "project implementation workflow" in text
    assert "documentation" in text
    assert "CI" in text
    assert "repository-level agent instructions" in text
    assert "source pointer" in text
    assert "concrete target" in text
    assert "proposed outcome" in text
    assert "independent implementation" in text


def test_reusable_tool_observation_stays_candidate() -> None:
    text = skill_text()
    assert "Skill candidates" in text
    assert "skill-retro" in text
    assert "cannot establish a recurring skill defect" in " ".join(text.split())


def test_review_does_not_write_project_or_agent_files() -> None:
    text = skill_text()
    assert "Do not modify files" in text
    assert "Do not modify any project, agent-instruction, or skill file" in text
