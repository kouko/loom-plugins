from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2] / 'skills' / 'skill-retro'


@pytest.mark.parametrize('name', ['README.md', 'README.ja.md', 'README.zh-TW.md'])
def test_readme_retains_usage_configuration_and_attribution(name):
    text = (ROOT / name).read_text()
    for heading in ('Installation', 'Quick start', 'Configuration'):
        assert f'## {heading}' in text
    assert 'Trace2Skill' in text
    assert 'Apache 2.0' in text
    assert 'skill-retro' in text
    assert 'scripts/apply.py' not in text
    assert '--approved' not in text
    assert 'scripts/main.py' in text
    assert 'scripts/propose.py' in text
