"""Tests for loom-code/hooks/language-anchor.py — the language-anchor hook.

concern: a reminder that goes silent on some trigger (an event, the Agent tool, a missing transcript, a mixed-script or non-zh/ja conversation) or that names one language or script again.

The hook detects nothing: on an accepted event (SessionStart,
UserPromptSubmit, or PostToolUse for the Skill or Agent tool) it emits one
fixed English reminder, whatever language the transcript holds and whether
or not a transcript exists. The replying model identifies the language.

Each test subprocess-runs the hook exactly as Claude Code would invoke it:
hook-event JSON on stdin, output on stdout, exit 0. Subprocess (not import)
is required — ``language-anchor.py`` is a hyphenated filename.

External surface grounded: the Claude Code hook contract (JSON event with
``hook_event_name`` / ``tool_name`` / ``transcript_path`` on stdin;
``hookSpecificOutput`` JSON on stdout when emitting, empty stdout
otherwise; exit 0), registered in ``loom-code/hooks/hooks.json``.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

HOOK = Path(__file__).resolve().parent.parent / "hooks" / "language-anchor.py"

ANCHOR = (
    "Write every message to the user in the language and script the user "
    "writes in during this conversation; machine-facing artifacts "
    "(brief/verdict/commit) keep their own language."
)

ZH_TURN = "請幫我確認這個修改是否符合原本的設計規範，並且說明理由。"
# Chinese dense with English terms: the per-letter count the old detector
# used read this as English and stayed silent.
ZH_WITH_TERMS = (
    "幫我看 loom-code 的 PostToolUse hook、SessionStart compact、"
    "transcript_path、additionalContext 跟 OpenCode loader 的 execute.after"
)


def _write_transcript(turns):
    """Write a JSONL transcript with one main-chain user turn per text."""
    fh = tempfile.NamedTemporaryFile(
        mode="w", suffix=".jsonl", delete=False, encoding="utf-8"
    )
    for text in turns:
        fh.write(json.dumps(
            {"type": "user", "isSidechain": False, "message": {"content": text}}
        ) + "\n")
    fh.close()
    return fh.name


def run_hook(payload):
    """Run the hook with `payload` (dict → JSON, str → raw) on stdin."""
    stdin = payload if isinstance(payload, str) else json.dumps(payload)
    return subprocess.run(
        [sys.executable, str(HOOK)], input=stdin, capture_output=True, text=True,
    )


def emitted(payload):
    """Run the hook and return (hookEventName, additionalContext)."""
    result = run_hook(payload)
    assert result.returncode == 0
    assert result.stdout, "anchor stayed silent"
    out = json.loads(result.stdout)["hookSpecificOutput"]
    return out["hookEventName"], out["additionalContext"]


def test_zh_with_english_terms_gets_anchor():
    transcript = _write_transcript([ZH_WITH_TERMS] * 3)
    assert emitted({"tool_name": "Skill", "transcript_path": transcript}) == (
        "PostToolUse", ANCHOR)


@pytest.mark.parametrize("turn", [
    "Please confirm this change matches the original design and explain why.",
    "이 변경 사항이 원래 설계와 일치하는지 확인하고 이유를 설명해 주세요.",
    "Merci de vérifier que cette modification respecte la conception d'origine.",
], ids=["en", "ko", "fr"])
def test_en_ko_fr_transcripts_get_same_text(turn):
    transcript = _write_transcript([turn] * 3)
    assert emitted({"tool_name": "Agent", "transcript_path": transcript})[1] == ANCHOR


def test_text_names_no_language_or_script():
    _, text = emitted({"tool_name": "Skill", "transcript_path": _write_transcript([ZH_TURN])})
    for name in ("中文", "日本語", "繁體", "繁体", "简体", "簡體",
                 "Chinese", "Japanese", "English", "Korean"):
        assert name not in text


def test_text_asks_for_user_language_and_script():
    _, text = emitted({"tool_name": "Skill", "transcript_path": _write_transcript([ZH_TURN])})
    assert "in the language and script the user writes in" in text


def test_missing_transcript_still_emits():
    assert emitted({"hook_event_name": "UserPromptSubmit"}) == ("UserPromptSubmit", ANCHOR)


def test_machine_artifact_clause_kept():
    event, text = emitted({"hook_event_name": "SessionStart", "source": "resume"})
    assert event == "SessionStart"
    assert "machine-facing artifacts (brief/verdict/commit) keep their own language" in text


def test_bash_tool_stays_silent():
    transcript = _write_transcript([ZH_TURN])
    result = run_hook({"tool_name": "Bash", "transcript_path": transcript})
    assert result.returncode == 0
    assert result.stdout == ""


@pytest.mark.parametrize("event", [["SessionStart"], "Stop", 7])
def test_unknown_hook_event_name_stays_silent(event):
    result = run_hook({"hook_event_name": event, "tool_name": "Skill"})
    assert result.returncode == 0
    assert result.stdout == ""


@pytest.mark.parametrize("stdin", ["not json {{{", "", "[1, 2]"],
                         ids=["malformed", "empty", "non-object"])
def test_malformed_stdin_stays_silent(stdin):
    result = run_hook(stdin)
    assert result.returncode == 0
    assert result.stdout == ""
