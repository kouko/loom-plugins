#!/usr/bin/env python3
"""Language anchor hook: PostToolUse (tool_name "Skill" or "Agent"),
SessionStart (compact / resume) and UserPromptSubmit — re-states the
conversation language.

Detects nothing: on an accepted event it emits one fixed English
``additionalContext`` reminder (``ANCHOR_TEXT``) asking the model to write
every user-facing message in the language and script the user writes in;
machine-facing artifacts (brief/verdict/commit) keep their own language.
The replying model identifies the language itself. No transcript is read.
Unknown events, other tools and malformed input resolve to no output,
exit 0 — this hook never blocks.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

_HOOKS_DIR = Path(__file__).resolve().parent
_LANG_DETECT_PATH = _HOOKS_DIR / "lang_detect.py"

ANCHOR_TEXT = (
    "Write every message to the user in the language and script the user "
    "writes in during this conversation; machine-facing artifacts "
    "(brief/verdict/commit) keep their own language."
)

# Temporary: read only by agy_adapter.py until it switches to ANCHOR_TEXT
# (W1-02); removed with lang_detect.py (W1-04).
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
    # Temporary: read only by agy_adapter.py until W1-02.
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

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": event,
            "additionalContext": ANCHOR_TEXT,
        }
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
