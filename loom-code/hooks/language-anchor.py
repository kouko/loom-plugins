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

import json
import sys

ANCHOR_TEXT = (
    "Write every message to the user in the language and script the user "
    "writes in during this conversation; machine-facing artifacts "
    "(brief/verdict/commit) keep their own language."
)


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
