#!/usr/bin/env python3
"""Language anchor hook: PostToolUse (tool_name "Skill" or "Agent"),
SessionStart (compact / resume) and UserPromptSubmit — re-states the
conversation language.

Detects the conversation language from the transcript (via
``lang_detect.conversation_language()``, reused by path — no target
language is ever hardcoded as a default) and, only when that detector
returns a majority 'ja' or 'zh' signal, emits an ``additionalContext``
directive in THAT language reminding the model to keep user-facing
narration in the conversation language (machine-facing artifacts —
brief/verdict/commit — stay as-is). 'en' / None / malformed input all
resolve to no output, exit 0 — this hook never blocks and never
selects a language on its own.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

_HOOKS_DIR = Path(__file__).resolve().parent
_LANG_DETECT_PATH = _HOOKS_DIR / "lang_detect.py"

# Directive text keyed by DETECTED language — emitted content, not a
# behavior selector (brief Non-goals: no hardcoded output language).
_ANCHOR_TEXT = {
    "zh": (
        "對使用者的敘述一律使用使用者在對話中所用的語言與文字；"
        "機器面 artifact（brief/verdict/commit）維持原語言。"
    ),
    "ja": (
        "ユーザー向けの説明は常にユーザーの会話言語（日本語）を使用してください。"
        "brief/verdict/commit などの機械向けアーティファクトは元の言語のままにします。"
    ),
}


def _load_lang_detect():
    spec = importlib.util.spec_from_file_location("lang_detect", _LANG_DETECT_PATH)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    try:
        payload = json.loads(sys.stdin.read())
    except ValueError:
        return 0
    if not isinstance(payload, dict):
        return 0
    event = payload.get("hook_event_name", "PostToolUse")
    if event not in ("SessionStart", "PostToolUse", "UserPromptSubmit"):
        return 0
    if event == "PostToolUse" and payload.get("tool_name") not in ("Skill", "Agent"):
        return 0
    transcript_path = payload.get("transcript_path")
    if not transcript_path:
        return 0

    try:
        lang_detect = _load_lang_detect()
        lang = lang_detect.conversation_language(transcript_path)
    except Exception:
        return 0

    text = _ANCHOR_TEXT.get(lang)
    if not text:
        return 0

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": event,
            "additionalContext": text,
        }
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
