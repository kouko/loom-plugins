"""Adversarial probes for the agy language anchor's current-turn look-back.

``hooks/agy_adapter.py`` now scans back to the latest USER_INPUT step and
anchors on the latest loom SKILL.md ``view_file`` in that span. These probes
feed hostile or boundary transcripts through the real adapter (subprocess,
TMPDIR isolated) and require: at most one anchor per skill read in the current
turn, never an anchor for an earlier turn, no crash, and first-turn session
context never lost. A failing probe is a finding against the change.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
ADAPTER = PLUGIN_ROOT / "hooks" / "agy_adapter.py"
JA_FRAGMENT = "会話言語（日本語）"
JA_TURN = "この変更が仕様に合っているかどうかを確認してください。よろしくお願いします。"
EN_TURN = "Please confirm this change matches the original design specification and explain why."
SKILL_A = "/Users/u/.gemini/config/plugins/loom-code/skills/build/SKILL.md"
SKILL_B = "/Users/u/.gemini/config/plugins/loom-workflow/skills/recap-state/SKILL.md"
OTHER_SKILL = "/Users/u/.gemini/config/plugins/other-plugin/skills/build/SKILL.md"


def _run(payload: dict, tmp_path: Path, timeout: int = 60) -> dict:
    env = {k: v for k, v in os.environ.items()
           if k not in ("LOOM_CODE_MODE", "ANTIGRAVITY_CONVERSATION_ID")}
    env["TMPDIR"] = str(tmp_path)
    result = subprocess.run([sys.executable, str(ADAPTER), "pre-invocation"],
                            input=json.dumps(payload), capture_output=True, text=True,
                            cwd=str(PLUGIN_ROOT), env=env, timeout=timeout)
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def _user(text: str, index=None) -> dict:
    step = {"source": "USER_EXPLICIT", "type": "USER_INPUT",
            "content": f"<USER_REQUEST>\n{text}\n</USER_REQUEST>"}
    if index is not None:
        step["step_index"] = index
    return step


def _view(path: str, index=None, quoted: bool = False) -> dict:
    value = json.dumps(path) if quoted else path
    step = {"source": "MODEL", "type": "PLANNER_RESPONSE",
            "tool_calls": [{"name": "view_file", "args": {"AbsolutePath": value}}]}
    if index is not None:
        step["step_index"] = index
    return step


def _result(index=None) -> dict:
    step = {"source": "MODEL", "type": "GENERIC", "content": "File Path: SKILL.md"}
    if index is not None:
        step["step_index"] = index
    return step


def _write(tmp_path: Path, steps: list, tail: str = "") -> Path:
    path = tmp_path / "transcript.jsonl"
    with path.open("w", encoding="utf-8") as fh:
        for step in steps:
            fh.write(json.dumps(step, ensure_ascii=False) + "\n")
        fh.write(tail)
    return path


def _payload(transcript: Path, num: int = 1, initial: int = 5) -> dict:
    return {"conversationId": "conv-adv", "workspacePaths": [], "invocationNum": num,
            "initialNumSteps": initial, "transcriptPath": str(transcript)}


def _anchors(out: dict) -> int:
    return sum(JA_FRAGMENT in s.get("ephemeralMessage", "") for s in out.get("injectSteps", []))


def test_anchor_no_user_input_no_anchor(tmp_path):
    """A transcript with skill reads but no USER_INPUT at all stays silent and exits cleanly."""
    transcript = _write(tmp_path, [_view(SKILL_A, 0), _result(1)])
    assert _run(_payload(transcript), tmp_path) == {}


def test_anchor_new_turn_after_skill_read_silent(tmp_path):
    """USER_INPUT after the view_file starts a new turn: the earlier read never anchors."""
    transcript = _write(tmp_path, [_user(JA_TURN, 0), _view(SKILL_A, 1), _result(2),
                                   _user(JA_TURN, 3)])
    assert _run(_payload(transcript), tmp_path) == {}


def test_anchor_earlier_english_turn_read_japanese_turn_silent(tmp_path):
    """A Japanese current turn without a read never anchors on an earlier turn's read."""
    transcript = _write(tmp_path, [_user(EN_TURN, 0), _view(SKILL_A, 1), _result(2),
                                   _user(JA_TURN, 3), _user(JA_TURN, 4),
                                   {"source": "MODEL", "type": "PLANNER_RESPONSE",
                                    "step_index": 5, "content": "thinking"}])
    assert _run(_payload(transcript), tmp_path) == {}


def test_anchor_previous_turn_read_then_english_turn_silent(tmp_path):
    """Anchored read in turn 1, then an English turn with no read: no repeat anchor."""
    steps = [_user(JA_TURN, 0), _view(SKILL_A, 1), _result(2)]
    assert _anchors(_run(_payload(_write(tmp_path, steps)), tmp_path)) == 1
    steps += [_user(EN_TURN, 3)]
    assert _run(_payload(_write(tmp_path, steps), num=0), tmp_path) == {}


def test_anchor_two_skills_one_turn_once_each(tmp_path):
    """Two different loom skills in one turn: one anchor per read, then silence."""
    steps = [_user(JA_TURN, 0), _view(SKILL_A, 1), _result(2)]
    counts = [_anchors(_run(_payload(_write(tmp_path, steps)), tmp_path))]
    steps += [_view(SKILL_B, 3, quoted=True), _result(4)]
    counts.append(_anchors(_run(_payload(_write(tmp_path, steps), num=2), tmp_path)))
    counts.append(_anchors(_run(_payload(_write(tmp_path, steps), num=3), tmp_path)))
    assert counts == [1, 1, 0]


def test_anchor_same_skill_duplicate_step_index_once(tmp_path):
    """The same skill read twice under a duplicated step_index anchors only once."""
    steps = [_user(JA_TURN, 0), _view(SKILL_A, 1), _result(2)]
    first = _anchors(_run(_payload(_write(tmp_path, steps)), tmp_path))
    steps += [_view(SKILL_A, 1), _result(2)]
    second = _anchors(_run(_payload(_write(tmp_path, steps), num=2), tmp_path))
    assert (first, second) == (1, 0)


def test_anchor_interleaved_non_loom_skill_still_anchors_once(tmp_path):
    """A non-loom SKILL.md read after the loom read neither hides nor repeats the anchor."""
    steps = [_user(JA_TURN, 0), _view(SKILL_A, 1), _view(OTHER_SKILL, 2), _result(3)]
    first = _anchors(_run(_payload(_write(tmp_path, steps)), tmp_path))
    steps += [_view(OTHER_SKILL, 4), _result(5)]
    second = _anchors(_run(_payload(_write(tmp_path, steps), num=2), tmp_path))
    assert (first, second) == (1, 0)


def test_anchor_partial_last_line_still_anchors(tmp_path):
    """A half-written trailing line (cut mid multibyte) neither crashes nor hides the read."""
    partial = json.dumps(_user(JA_TURN, 3), ensure_ascii=False).encode("utf-8")[:40]
    path = _write(tmp_path, [_user(JA_TURN, 0), _view(SKILL_A, 1), _result(2)])
    with path.open("ab") as fh:
        fh.write(partial)
    assert _anchors(_run(_payload(path), tmp_path)) == 1


def test_anchor_thousands_of_steps_single_anchor_promptly(tmp_path):
    """3000 earlier turns with reads plus a final read: one anchor, well inside a hook timeout."""
    steps = []
    index = 0
    for _ in range(3000):
        steps += [_user(JA_TURN, index), _view(SKILL_A, index + 1), _result(index + 2)]
        index += 3
    steps += [_user(JA_TURN, index), _view(SKILL_B, index + 1), _result(index + 2)]
    transcript = _write(tmp_path, steps)
    start = time.monotonic()
    first = _anchors(_run(_payload(transcript), tmp_path))
    second = _anchors(_run(_payload(transcript, num=2), tmp_path))
    assert (first, second) == (1, 0)
    assert time.monotonic() - start < 20


def test_anchor_null_step_index_across_turns_anchors_each_turn(tmp_path):
    """Explicit null step_index must not make a later turn's read look already anchored."""
    steps = [_user(JA_TURN, None), _view(SKILL_A, None), _result(None)]
    for step in steps:
        step["step_index"] = None
    first = _anchors(_run(_payload(_write(tmp_path, steps)), tmp_path))
    later = [_user(JA_TURN), _view(SKILL_B), _result()]
    for step in later:
        step["step_index"] = None
    second = _anchors(_run(_payload(_write(tmp_path, steps + later), num=1), tmp_path))
    assert (first, second) == (1, 1)


def test_anchor_non_integer_step_index_no_crash(tmp_path):
    """A dict-valued step_index is tolerated: one anchor, then silence."""
    steps = [_user(JA_TURN, 0), _view(SKILL_A, {"x": [1, "二"]}), _result("3")]
    first = _anchors(_run(_payload(_write(tmp_path, steps)), tmp_path))
    second = _anchors(_run(_payload(_write(tmp_path, steps), num=2), tmp_path))
    assert (first, second) == (1, 0)


def test_anchor_malformed_later_step_keeps_first_turn_context(tmp_path):
    """A MODEL step with non-list tool_calls after the read: first-turn session context survives."""
    steps = [_user(JA_TURN, 0), _view(SKILL_A, 1), {"source": "MODEL", "type": "GENERIC",
                                                    "step_index": 2, "tool_calls": 5}]
    out = _run(_payload(_write(tmp_path, steps), num=0, initial=1), tmp_path)
    messages = [s["ephemeralMessage"] for s in out.get("injectSteps", [])]
    assert any("Station order:" in m for m in messages), out


def test_anchor_malformed_later_step_still_anchors(tmp_path):
    """A MODEL step with non-list tool_calls after the loom read must not drop the anchor."""
    steps = [_user(JA_TURN, 0), _view(SKILL_A, 1), {"source": "MODEL", "type": "GENERIC",
                                                    "step_index": 2, "tool_calls": 5}]
    assert _anchors(_run(_payload(_write(tmp_path, steps)), tmp_path)) == 1
