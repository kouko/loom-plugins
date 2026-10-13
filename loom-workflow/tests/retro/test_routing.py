"""Retro and distill-sessions remain separate discovery routes."""

# concern: single-session project retrospectives must not displace recurring skill mining.

from pathlib import Path


SKILLS = Path(__file__).resolve().parents[2] / "skills"
ROUTER = SKILLS / "using-loom-workflow" / "SKILL.md"
DISTILL = SKILLS / "distill-sessions" / "SKILL.md"


def test_single_session_retro_and_cross_session_skill_mining_have_distinct_routes():
    text = ROUTER.read_text(encoding="utf-8")
    assert "Review the current or one specified coding session for project development improvements | [retro](../retro/SKILL.md)" in text
    assert "Mine past agent sessions or skill-activation telemetry for improvement evidence | [distill-sessions](../distill-sessions/SKILL.md)" in text
    assert text.count("[retro](../retro/SKILL.md)") == 1
    assert text.count("[distill-sessions](../distill-sessions/SKILL.md)") == 1


def test_distill_sessions_contract_still_targets_recurring_skill_issues():
    text = DISTILL.read_text(encoding="utf-8")
    assert "name: distill-sessions" in text
    assert "recurring friction" in text
    assert "Mine completed Claude Code and Codex sessions" in text
    assert "a single-session reflection" in text
