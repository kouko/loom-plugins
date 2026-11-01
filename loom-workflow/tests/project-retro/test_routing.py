"""Project and skill retrospectives have distinct discovery routes."""

# concern: single-session project retrospectives must not displace recurring skill mining.

from pathlib import Path
import re


SKILLS = Path(__file__).resolve().parents[2] / "skills"
ROUTER = SKILLS / "using-loom-workflow" / "SKILL.md"
SKILL_RETRO = SKILLS / "skill-retro" / "SKILL.md"


def test_single_session_retro_and_cross_session_skill_mining_have_distinct_routes():
    text = ROUTER.read_text(encoding="utf-8")
    assert "Review the current or one specified coding session for project development improvements, or 振り返り seeking project development improvements | [project-retro](../project-retro/SKILL.md)" in text
    row = next(line for line in text.splitlines() if '[skill-retro]' in line)
    def allows_skill_review(candidate):
        return bool(re.search(r'Review .*past or current.*recurring.*readable.*skill.*integration', candidate)) and not re.search(r'\b(?:no|not|never|forbid\w*|prohibit\w*|installed)\b', candidate, re.I)

    example = 'Review past or current snapshots for recurring issues in readable skill sources and integration.'
    assert allows_skill_review(example)
    assert not allows_skill_review('Do not ' + example)
    assert allows_skill_review(row)
    assert text.count("[project-retro](../project-retro/SKILL.md)") == 1
    assert text.count("[skill-retro](../skill-retro/SKILL.md)") == 1
    assert "[retro](" not in text
    assert "[distill-sessions](" not in text


def test_skill_retro_contract_targets_recurring_skill_issues():
    text = SKILL_RETRO.read_text(encoding="utf-8")
    assert "name: skill-retro" in text
    opening = text.split('## Privacy', 1)[0]
    assert re.search(r'Review selected past or current.*readable target skill', opening)
    assert 'captured snapshot' in opening and 'cutoff' in opening
    assert re.search(r'Two distinct sessions promote .*one session remains pending', text)
    assert "plugin registration" in text
    for name, terms in [
        ('README.md', ('past or current', 'readable', 'snapshot', 'integration')),
        ('README.ja.md', ('過去または現在', '読み取り可能', 'スナップショット', '統合')),
        ('README.zh-TW.md', ('過去或目前', '可讀取', '快照', '整合')),
    ]:
        readme = (SKILLS.parent / name).read_text()
        row = next(line for line in readme.splitlines() if '[`skill-retro`]' in line)
        assert all(term in row for term in terms)


def test_japanese_furikaeri_routes_by_requested_purpose():
    router = ROUTER.read_text(encoding="utf-8")
    recap = (SKILLS / "recap-state" / "SKILL.md").read_text(encoding="utf-8")
    retro = (SKILLS / "project-retro" / "SKILL.md").read_text(encoding="utf-8")
    assert "振り返り when asking where the current conversation stands" in router
    assert "振り返り seeking project development improvements" in router
    assert "in-session recap of current progress" in recap
    assert "'振り返り'" in recap
    assert "振り返り seeking improvements" in retro
