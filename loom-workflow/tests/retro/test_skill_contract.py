"""Observable contract for the user-invoked single-session retro skill."""

from pathlib import Path


SKILL = Path(__file__).resolve().parents[2] / "skills" / "retro" / "SKILL.md"


def skill_text() -> str:
    assert SKILL.is_file(), "retro must ship as a skill"
    return SKILL.read_text(encoding="utf-8")


def test_user_invoked_current_or_specified_session() -> None:
    text = skill_text()
    assert "name: retro" in text
    assert "user-invocable: true" in text
    assert "current session" in text
    assert "specified session" in text
    assert "one coding session" in text


def test_ranked_recommendations_link_to_observed_source() -> None:
    text = skill_text()
    assert "rank" in text.lower()
    assert "impact" in text.lower()
    assert "source" in text.lower()
    assert "event" in text.lower()
    assert "recommendation" in text.lower()
    assert "existing checks" in text.lower()


def test_missing_source_limits_claims() -> None:
    text = skill_text()
    assert "unavailable" in text.lower()
    assert "do not invent" in text.lower()
    assert "cannot substantiate" in text.lower()


def test_project_advice_is_separate_from_skill_candidates_and_read_only() -> None:
    text = skill_text()
    assert "Project recommendations" in text
    assert "Skill candidates" in text
    assert "read-only" in text.lower()
    assert "do not modify" in text.lower()
    assert "single session" in text.lower()
    assert "distill-sessions" in text


def test_read_only_shell_inspection_remains_available() -> None:
    text = skill_text()
    assert "write-capable tool" not in text
    assert "Do not modify files" in text


def test_sensitive_transcript_handling_names_model_context_boundary() -> None:
    text = skill_text()
    assert "Keep sensitive transcript text local" not in text
    assert "tool output enters the model context" in text
    assert "redact secrets locally before any excerpt appears in tool output" in text
    assert "redacted excerpt" in text
