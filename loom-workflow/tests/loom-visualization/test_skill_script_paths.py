"""Bundled scripts must be run from the skill directory on every host.

A bare `python3 scripts/<name>.py` resolves against the working directory,
which is not the skill folder on Claude Code or Antigravity CLI. Each skill
defines a `<skill-dir>` token once in SKILL.md and every command uses it.
"""

import re
import sys
from pathlib import Path

SKILLS = Path(__file__).resolve().parents[2] / "skills"
SKILL_DIRS = [SKILLS / "loom-visualization", SKILLS / "goal-create"]

# One matcher for the whole repo: the contract-citation lint's own, so this
# test cannot drift weaker than the gate.
sys.path.insert(0, str(SKILLS.parent.parent / "loom-code" / "scripts"))
from check_contract_citations import find_bare_script_paths  # noqa: E402

SKILL_DIR_SCRIPT = re.compile(r"<skill-dir>/scripts/([\w.-]+)")


def _markdown(skill_dir):
    return sorted(skill_dir.rglob("*.md"))


def test_skill_dir_phrase_defined_and_used_for_every_script_call():
    for skill_dir in SKILL_DIRS:
        prose = " ".join((skill_dir / "SKILL.md").read_text(encoding="utf-8").split())
        assert "`<skill-dir>` is this skill's folder" in prose, skill_dir.name
        assert "`${CLAUDE_SKILL_DIR}` on Claude Code" in prose, skill_dir.name
        assert "on any other host, the directory that holds this SKILL.md" in prose, skill_dir.name
        assert SKILL_DIR_SCRIPT.search(prose), skill_dir.name


def test_bare_scripts_path_left_in_skill_doc():
    # The matcher must still see the bare forms, or an empty result is vacuous.
    assert find_bare_script_paths("python3 scripts/render.py") == [1]
    assert find_bare_script_paths('python3.12 -X utf8 "./scripts/x.py"') == [1]
    assert find_bare_script_paths("python3 <skill-dir>/scripts/render.py") == []

    offenders = [
        f"{path.relative_to(SKILLS)}:{n}"
        for skill_dir in SKILL_DIRS
        for path in _markdown(skill_dir)
        for n in find_bare_script_paths(path.read_text(encoding="utf-8"))
    ]
    assert not offenders, offenders


def test_every_skill_dir_script_reference_exists():
    for skill_dir in SKILL_DIRS:
        for path in _markdown(skill_dir):
            for name in SKILL_DIR_SCRIPT.findall(path.read_text(encoding="utf-8")):
                assert (skill_dir / "scripts" / name).is_file(), f"{path}: {name}"


def test_non_skill_docs_using_the_token_point_to_skill_md():
    for skill_dir in SKILL_DIRS:
        for path in _markdown(skill_dir):
            text = path.read_text(encoding="utf-8")
            if path.name != "SKILL.md" and "<skill-dir>" in text:
                assert "defined in `SKILL.md`" in " ".join(text.split()), path
