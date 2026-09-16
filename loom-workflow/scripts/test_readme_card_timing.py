"""A10/A2: the READMEs describe when the visualization card arrives, and where not.

Positive: every loom-workflow README names the hosts the per-turn reminder
does not reach (Codex IDE extension and app, Antigravity desktop app and IDE)
and the loom-code-only install, and every current description calls the card
by the name its own header uses. Negative: no README, and not the Codex
manifest's long description, still says the card arrives at SessionStart, and
none of the three languages reintroduces the old "trigger card" name; the
per-turn word figure is not smaller than the committed cards.
"""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path

PLUGIN_DIR = Path(__file__).resolve().parents[1]

# Per-language phrases that must appear in each README's install limits note.
LIMIT_PHRASES = {
    "README.md": (
        "Codex IDE extension",
        "Codex app",
        "Antigravity desktop app or IDE",
        "`loom-code` without `loom-workflow`",
    ),
    "README.ja.md": (
        "Codex の IDE 拡張",
        "Codex アプリ",
        "Antigravity のデスクトップアプリや IDE",
        "`loom-workflow` なしで `loom-code`",
    ),
    "README.zh-TW.md": (
        "Codex IDE 擴充功能",
        "Codex app",
        "Antigravity 桌面 app 與 IDE",
        "只裝 `loom-code`、沒裝 `loom-workflow`",
    ),
}

STALE_TIMING = re.compile(
    r"SessionStart|session[ -]start|startup, clear, and compact"
    r"|セッション開始時|工作階段開始時|session 開始時",
    re.I,
)


# The name the cards' own headers use: "# Visualization card (loom-workflow)".
CURRENT_NAME = "visualization card"

# The name the cards dropped; historical CHANGELOG entries keep it, current
# descriptions must not, in any of the three languages.
OLD_NAME = re.compile(r"trigger card|トリガーカード|觸發卡", re.I)

READMES = ("README.md", "README.ja.md", "README.zh-TW.md")

CARD_ASSETS = (
    "skills/loom-visualization/assets/trigger-card.md",
    "skills/loom-visualization/assets/trigger-card-coexist.md",
)

# The per-turn word figure each README states, in its own language.
WORD_FIGURE = {
    "README.md": re.compile(r"(\d+) words per turn"),
    "README.ja.md": re.compile(r"(\d+)\s*語"),
    "README.zh-TW.md": re.compile(r"(\d+)\s*個英文字"),
}


def _read(name: str) -> str:
    return (PLUGIN_DIR / name).read_text(encoding="utf-8")


def _missing_limits(text: str, phrases: tuple[str, ...]) -> list[str]:
    return [p for p in phrases if p not in text]


def _stale_lines(text: str) -> list[str]:
    return [line for line in text.splitlines() if STALE_TIMING.search(line)]


def _old_name_lines(text: str) -> list[str]:
    return [line for line in text.splitlines() if OLD_NAME.search(line)]


def _hook_docstring() -> str:
    source = (PLUGIN_DIR / "hooks" / "visualization-card").read_text(encoding="utf-8")
    return ast.get_docstring(ast.parse(source)) or ""


def test_current_descriptions_use_the_cards_own_name() -> None:
    for name in READMES:
        text = _read(name)
        assert CURRENT_NAME in text, name
        assert _old_name_lines(text) == [], name
    codex = json.loads(_read(".codex-plugin/plugin.json"))
    described = codex["interface"]["longDescription"]
    assert CURRENT_NAME in described
    assert _old_name_lines(described) == []
    docstring = _hook_docstring()
    assert CURRENT_NAME in docstring.lower()
    assert _old_name_lines(docstring) == []


def test_per_turn_word_figure_is_not_below_the_committed_cards() -> None:
    longest = max(len(_read(asset).split()) for asset in CARD_ASSETS)
    for name, pattern in WORD_FIGURE.items():
        match = pattern.search(_read(name))
        assert match is not None, name
        assert int(match.group(1)) >= longest, (name, match.group(1), longest)


def test_readmes_state_unreached_hosts_and_loom_code_only() -> None:
    for name, phrases in LIMIT_PHRASES.items():
        text = _read(name)
        assert _missing_limits(text, phrases) == [], name
        assert "UserPromptSubmit" in text, name


def test_sessionstart_wording_removed() -> None:
    for name in LIMIT_PHRASES:
        assert _stale_lines(_read(name)) == [], name
    codex = json.loads(_read(".codex-plugin/plugin.json"))
    assert _stale_lines(codex["interface"]["longDescription"]) == []


def test_checks_catch_stale_and_missing_wording() -> None:
    stale = "intro\n│   └── visualization-card SessionStart trigger card\n"
    assert _stale_lines(stale) == ["│   └── visualization-card SessionStart trigger card"]
    for line in ("The card also arrives at session-start.",
                 "カードはセッション開始時に一度だけ届く。",
                 "卡片只在工作階段開始時送達一次。",
                 "卡片在 session 開始時送達。"):
        assert _stale_lines("intro\n" + line + "\n") == [line], line
    assert _stale_lines("The card arrives with every message you send.\n") == []
    for line in ("the loom-visualization trigger card arrives on every message",
                 "loom-visualization のトリガーカードを届ける",
                 "loom-visualization 的觸發卡以 plugin rule 送達",
                 "loom-visualization 的觸發卡片"):
        assert _old_name_lines("intro\n" + line + "\n") == [line], line
    assert _old_name_lines("the loom-visualization visualization card\n") == []
    assert _missing_limits("Codex app only", LIMIT_PHRASES["README.md"]) == [
        "Codex IDE extension",
        "Antigravity desktop app or IDE",
        "`loom-code` without `loom-workflow`",
    ]
