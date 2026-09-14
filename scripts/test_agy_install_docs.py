"""Antigravity CLI (agy) install documentation and host principles.

Acceptance 1: the written install steps take a fresh clone to three installed
plugins (clone, then `agy plugin install <dir>` per plugin, loom-code first),
with no claim of an Antigravity marketplace. Acceptance 9: PRINCIPLES.md names
Antigravity CLI as a host without changing the Non-negotiables count.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGINS = ("loom-code", "loom-design", "loom-workflow")
CLONE = "git clone https://github.com/kouko/loom-plugins.git"

# Every README that carries an agy install section (English, plus translated
# siblings that already carry a Codex install section).
AGY_READMES = (
    "README.md",
    "loom-code/README.md",
    "loom-code/README.ja.md",
    "loom-code/README.zh-TW.md",
    "loom-design/README.md",
    "loom-design/README.ja.md",
    "loom-design/README.zh-TW.md",
    "loom-workflow/README.md",
)


def _read(rel: str) -> str:
    return (REPO_ROOT / rel).read_text(encoding="utf-8")


def _agy_section(text: str) -> str:
    match = re.search(r"^### Antigravity CLI\n(.*?)(?=^#{1,3} )", text, re.S | re.M)
    assert match, "no '### Antigravity CLI' section"
    return match.group(1)


def test_readme_agy_install_steps_from_clone() -> None:
    section = _agy_section(_read("README.md"))
    positions = [section.find(CLONE)]
    positions += [section.find(f"agy plugin install ./{p}") for p in PLUGINS]
    assert -1 not in positions, positions
    assert positions == sorted(positions), "clone, then loom-code, loom-design, loom-workflow"
    for command in ("agy plugin list", "agy plugin validate", "agy plugin uninstall", "git pull"):
        assert command in section, command
    assert "closing-review" in section
    assert "Gemini" in section
    for rel in AGY_READMES[1:]:
        plugin = rel.split("/")[0]
        body = _agy_section(_read(rel))
        assert CLONE in body, rel
        assert f"agy plugin install ./{plugin}" in body, rel
        if plugin != "loom-code":  # loom-design and loom-workflow skills refer to loom-code
            assert -1 < body.find("agy plugin install ./loom-code") < body.find(
                f"agy plugin install ./{plugin}"
            ), rel
    assert "Install `loom-code` first." in _agy_section(_read("loom-workflow/README.md"))


# The agy hook parenthetical in each loom-code README names its third hook.
LANGUAGE_REMINDER = {
    "loom-code/README.md": "language reminder",
    "loom-code/README.ja.md": "言語リマインダー",
    "loom-code/README.zh-TW.md": "語言提醒",
}


def test_loom_code_readmes_list_language_reminder_hook() -> None:
    for rel, phrase in LANGUAGE_REMINDER.items():
        assert phrase in _agy_section(_read(rel)), rel


def test_manifest_descriptions_name_antigravity_cli() -> None:
    import json

    for plugin in ("loom-code", "loom-design"):
        manifest = json.loads(_read(f"{plugin}/.claude-plugin/plugin.json"))
        assert manifest["description"].endswith("Claude Code, Codex + Antigravity CLI."), plugin


def test_readme_claims_agy_marketplace() -> None:
    for rel in AGY_READMES:
        for line in _read(rel).splitlines():
            if "agy" in line:
                assert "marketplace" not in line.lower(), (rel, line)
                assert not re.search(r"agy plugin \w+ \S+@\S+", line), (rel, line)


def test_principles_name_antigravity_cli() -> None:
    text = _read("PRINCIPLES.md")
    who = re.search(r"^## Who\n(.*?)^## ", text, re.S | re.M).group(1)
    assert "Antigravity CLI" in who
    hooks = next(l for l in text.splitlines() if l.startswith("- Host-installed plugin hooks"))
    assert "Antigravity CLI" in hooks
    ratified = next(l for l in text.splitlines() if l.startswith("ratified-by:"))
    assert "Antigravity CLI added) by kouko 2026-09-14" in ratified


def test_principles_non_negotiables_count_unchanged() -> None:
    text = _read("PRINCIPLES.md")
    body = re.search(r"^## Non-negotiables \(ordered\)\n(.*?)^## ", text, re.S | re.M).group(1)
    assert len(re.findall(r"^\d+\. ", body, re.M)) == 5
