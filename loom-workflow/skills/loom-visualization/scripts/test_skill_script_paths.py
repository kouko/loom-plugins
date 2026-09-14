"""Bundled scripts must be run from the skill directory on every host.

A bare `python3 scripts/<name>.py` resolves against the working directory,
which is not the skill folder on Claude Code or Antigravity CLI. Each skill
defines a `<skill-dir>` token once in SKILL.md and every command uses it.
"""

import re
from pathlib import Path

SKILLS = Path(__file__).resolve().parent.parent.parent
SKILL_DIRS = [SKILLS / "loom-visualization", SKILLS / "goal-create"]

BARE_COMMAND = re.compile(r"\b(?:python3|bash|sh) (?:\./)?scripts/")
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
    offenders = [
        f"{path.relative_to(SKILLS)}:{n}"
        for skill_dir in SKILL_DIRS
        for path in _markdown(skill_dir)
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1)
        if BARE_COMMAND.search(line)
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
