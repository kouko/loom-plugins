"""Project and skill retrospectives have distinct discovery routes."""

# concern: single-session project retrospectives must not displace recurring skill mining.

from pathlib import Path


SKILLS = Path(__file__).resolve().parents[2] / "skills"
ROUTER = SKILLS / "using-loom-workflow" / "SKILL.md"
SKILL_RETRO = SKILLS / "skill-retro" / "SKILL.md"


def test_single_session_retro_and_cross_session_skill_mining_have_distinct_routes():
    text = ROUTER.read_text(encoding="utf-8")
    assert "Review the current or one specified coding session for project development improvements, or 振り返り seeking project development improvements | [project-retro](../project-retro/SKILL.md)" in text
    assert "Review several sessions for recurring issues in an installed skill or its related plugin integration | [skill-retro](../skill-retro/SKILL.md)" in text
    assert text.count("[project-retro](../project-retro/SKILL.md)") == 1
    assert text.count("[skill-retro](../skill-retro/SKILL.md)") == 1
    assert "[retro](" not in text
    assert "[distill-sessions](" not in text


def test_skill_retro_contract_targets_recurring_skill_issues():
    text = SKILL_RETRO.read_text(encoding="utf-8")
    assert "name: skill-retro" in text
    assert "several completed sessions" in text
    assert "plugin registration" in text


def test_japanese_furikaeri_routes_by_requested_purpose():
    router = ROUTER.read_text(encoding="utf-8")
    recap = (SKILLS / "recap-state" / "SKILL.md").read_text(encoding="utf-8")
    retro = (SKILLS / "project-retro" / "SKILL.md").read_text(encoding="utf-8")
    assert "振り返り when asking where the current conversation stands" in router
    assert "振り返り seeking project development improvements" in router
    assert "in-session recap of current progress" in recap
    assert "'振り返り'" in recap
    assert "振り返り seeking improvements" in retro
