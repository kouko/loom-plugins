"""A10: the READMEs describe when the trigger card arrives, and where it does not.

Positive: every loom-workflow README names the hosts the per-turn reminder
does not reach (Codex IDE extension and app, Antigravity desktop app and IDE)
and the loom-code-only install. Negative: no README, and not the Codex
manifest's long description, still says the card arrives at SessionStart.
"""

from __future__ import annotations

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


def _read(name: str) -> str:
    return (PLUGIN_DIR / name).read_text(encoding="utf-8")


def _missing_limits(text: str, phrases: tuple[str, ...]) -> list[str]:
    return [p for p in phrases if p not in text]


def _stale_lines(text: str) -> list[str]:
    return [line for line in text.splitlines() if STALE_TIMING.search(line)]


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
    assert _missing_limits("Codex app only", LIMIT_PHRASES["README.md"]) == [
        "Codex IDE extension",
        "Antigravity desktop app or IDE",
        "`loom-code` without `loom-workflow`",
    ]
