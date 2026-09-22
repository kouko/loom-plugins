"""Antigravity CLI (agy) hook adapter for loom-code.

Each test runs ``hooks/agy_adapter.py`` the way agy 1.2.2 does: ``sh -c``
from the plugin root, camelCase event JSON on stdin, one JSON object on
stdout, exit 0. The adapter translates agy payloads into the existing
handlers (the loom checker push rule, ``hooks/session-start``,
``hooks/language-anchor.py`` + ``hooks/lang_detect.py``).

External surfaces grounded (live agy 1.2.2 spikes, recorded in this change's
plan risk notes): PreToolUse ``toolCall.args.CommandLine`` / ``args.Cwd`` and
``{"decision": "allow"|"deny", "reason"}``; PreInvocation ``invocationNum``
and ``{"injectSteps": [{"ephemeralMessage": ...}]}``; transcript JSONL steps
``{step_index, source, type, content | tool_calls}`` with user text wrapped in
``<USER_REQUEST>``; skills are read through ``view_file`` ``AbsolutePath``.
"""
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
ADAPTER = PLUGIN_ROOT / "hooks" / "agy_adapter.py"

JA_FRAGMENT = "会話言語（日本語）"
ZH_FRAGMENT = "會話語言（繁體中文）"
JA_TURN = "この変更が仕様に合っているかどうかを確認してください。よろしくお願いします。"
ZH_TURN = "請幫我確認這個修改是否符合原本的設計規範，並且說明理由。"
EN_TURN = "Please confirm this change matches the original design specification and explain why."
LOOM_SKILL = "/Users/u/.gemini/config/plugins/loom-code/skills/build/SKILL.md"


def _run(mode: str, payload: dict, tmp_path: Path, adapter: Path = ADAPTER, **env):
    environ = {k: v for k, v in os.environ.items() if k != "LOOM_CODE_MODE"}
    environ.update(TMPDIR=str(tmp_path), **env)
    result = subprocess.run(
        [sys.executable, str(adapter), mode],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        cwd=adapter.parent.parent,
        env=environ,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def _git(repo: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@example.com", *args],
        cwd=repo, check=True, capture_output=True,
    )


@pytest.fixture
def change_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "commit", "-q", "--allow-empty", "-m", "init")
    _git(repo, "checkout", "-q", "-b", "feat")
    (repo / "f.txt").write_text("x\n")
    _git(repo, "add", "f.txt")
    _git(repo, "commit", "-q", "-m", "change")
    return repo


def _tool_payload(command: str, cwd: str, workspace: list[str]) -> dict:
    return {
        "conversationId": "c1",
        "workspacePaths": workspace,
        "toolCall": {"name": "run_command", "args": {"CommandLine": command, "Cwd": cwd}},
        "stepIdx": 3,
    }


# --- acceptance 4: push gate ------------------------------------------------

def test_push_with_running_checker_allows_and_forwards_reminder(change_repo, tmp_path):
    """The checker allows a push of an unidentified change and prints one
    reminder line; the adapter allows and carries that line as the reason."""
    out = _run("push-gate", _tool_payload("git push origin feat", ".", [str(change_repo)]), tmp_path)
    assert out["decision"] == "allow", out
    assert out["reason"].startswith("loom: "), out


def test_selection_store_write_with_running_checker_denies(change_repo, tmp_path):
    out = _run("push-gate", _tool_payload("echo x >> .git/loom/selections/c.jsonl", ".",
                                          [str(change_repo)]), tmp_path)
    assert out["decision"] == "deny"
    assert "BLOCK selection.guard" in out["reason"]


def test_non_push_command_returns_allow(change_repo, tmp_path):
    out = _run("push-gate", _tool_payload("git status", ".", [str(change_repo)]), tmp_path)
    assert out == {"decision": "allow"}


@pytest.fixture
def checkerless_adapter(tmp_path: Path) -> Path:
    root = tmp_path / "plugin"
    (root / "hooks").mkdir(parents=True)
    shutil.copy2(ADAPTER, root / "hooks" / "agy_adapter.py")
    return root / "hooks" / "agy_adapter.py"


def _codex_fallback(payload: dict, tmp_path: Path, matcher: int = 0) -> subprocess.CompletedProcess:
    """Run a Codex PreToolUse command with its plugin root removed."""
    hooks = json.loads((PLUGIN_ROOT / "hooks" / "hooks-codex.json").read_text(encoding="utf-8"))
    command = hooks["hooks"]["PreToolUse"][matcher]["hooks"][0]["command"]
    return subprocess.run(
        ["sh", "-c", command], input=json.dumps(payload), capture_output=True, text=True,
        timeout=30, env={**os.environ, "PLUGIN_ROOT": str(tmp_path / "removed-version")},
    )


FAILED_ALLOWING = "loom: publication hook failed ("


@pytest.mark.parametrize("command", ["git push origin feat", "gh pr create --fill"])
def test_missing_checker_allows_push_on_both_hosts(checkerless_adapter, change_repo, tmp_path, command):
    out = _run("push-gate", _tool_payload(command, ".", [str(change_repo)]), tmp_path,
               adapter=checkerless_adapter)
    assert out["decision"] == "allow", out
    assert out["reason"].startswith(FAILED_ALLOWING) and out["reason"].endswith("; allowing."), out
    codex = _codex_fallback({"tool_name": "Bash", "tool_input": {"command": command}}, tmp_path)
    assert codex.returncode == 0, codex.stderr
    assert FAILED_ALLOWING in codex.stderr and "; allowing." in codex.stderr


SELECTION_WRITE = "echo x >> .git/loom/selections/c.jsonl"


def test_missing_checker_denies_selection_store_write(checkerless_adapter, change_repo, tmp_path):
    out = _run("push-gate", _tool_payload(SELECTION_WRITE, ".", [str(change_repo)]), tmp_path,
               adapter=checkerless_adapter)
    assert out["decision"] == "deny", out
    assert "BLOCK selection.guard" in out["reason"]
    bash = _codex_fallback({"tool_name": "Bash", "tool_input": {"command": SELECTION_WRITE}}, tmp_path)
    assert bash.returncode == 2 and "BLOCK selection.guard" in bash.stderr
    for tool_name, tool_input in [
        ("Write", {"file_path": ".git/loom/selections/c.jsonl", "content": "{}"}),
        ("Edit", {"file_path": "/r/.git/loom/selections/c.jsonl", "old_string": "a", "new_string": "b"}),
        ("apply_patch", {"command": "*** Begin Patch\n*** Add File: .git/loom/selections/c.jsonl\n+{}\n"
                                    "*** End Patch\n"}),
    ]:
        result = _codex_fallback({"tool_name": tool_name, "tool_input": tool_input}, tmp_path, matcher=1)
        assert result.returncode == 2, (tool_name, result.stderr)
        assert "BLOCK selection.guard" in result.stderr


def test_missing_checker_allows_ordinary_file_write_on_codex(tmp_path):
    """Only a selection-store target is denied: content naming the store is not a target."""
    result = _codex_fallback({"tool_name": "Write", "tool_input": {
        "file_path": "notes.md", "content": "see .git/loom/selections/"}}, tmp_path, matcher=1)
    assert result.returncode == 0, result.stderr


# Store writes whose text never spells the literal store path; the running
# guard's ALWAYS_DENIED patterns (`loom/selections/`, `\.git/loom`) refuse them.
UNSPELLED_STORE_WRITES = [
    "cd .git/loom && printf x > selections/c.jsonl",
    "printf x > .git/loom//selections/c.jsonl",
    "printf x > .git/loom/./selections/c.jsonl",
]


@pytest.mark.parametrize("command", UNSPELLED_STORE_WRITES)
def test_missing_checker_denies_unspelled_store_write(checkerless_adapter, change_repo, tmp_path, command):
    out = _run("push-gate", _tool_payload(command, ".", [str(change_repo)]), tmp_path,
               adapter=checkerless_adapter)
    assert out["decision"] == "deny", out
    codex = _codex_fallback({"tool_name": "Bash", "tool_input": {"command": command}}, tmp_path)
    assert codex.returncode == 2 and "BLOCK selection.guard" in codex.stderr, codex.stderr


# Store writes the running guard refuses although their text never spells the
# store path: a git-directory lookup, a bare selections/ path, or a cwd inside
# the store that a relative target or command runs from.
CWD_STORE_WRITES = [
    ("Bash", {"command": "cd $(git rev-parse --git-dir)/loom; printf x > selections/c.jsonl"}, "."),
    ("Bash", {"command": "printf x > selections/c.jsonl"}, ".git/loom"),
    ("Write", {"file_path": "selections/c.jsonl", "content": "{}"}, ".git/loom"),
    ("apply_patch", {"command": "*** Begin Patch\n*** Add File: selections/c.jsonl\n+{}\n"
                                "*** End Patch\n"}, ".git/loom"),
]


@pytest.mark.parametrize("tool_name,tool_input,cwd", CWD_STORE_WRITES)
def test_missing_checker_denies_store_write_from_cwd(checkerless_adapter, change_repo, tmp_path,
                                                     tool_name, tool_input, cwd):
    payload = {"tool_name": tool_name, "tool_input": tool_input,
               "cwd": os.path.normpath(change_repo / cwd)}
    codex = _codex_fallback(payload, tmp_path, matcher=0 if tool_name == "Bash" else 1)
    assert codex.returncode == 2 and "BLOCK selection.guard" in codex.stderr, codex.stderr
    if tool_name == "Bash":  # agy's push gate sees run_command only
        out = _run("push-gate", _tool_payload(tool_input["command"], cwd, [str(change_repo)]),
                   tmp_path, adapter=checkerless_adapter)
        assert out["decision"] == "deny", out
        assert "BLOCK selection.guard" in out["reason"]


def test_fallback_patterns_mirror_selection_guard():
    """The agy fallback refuses on exactly the running guard's patterns."""
    sys.path.insert(0, str(PLUGIN_ROOT / "scripts"))
    from loom_checker.rule_checks import selection_guard as guard

    spec = importlib.util.spec_from_file_location("agy_adapter", ADAPTER)
    adapter = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(adapter)
    assert [p.pattern for p in adapter.SELECTION_STORE] == [p.pattern for p, _ in guard.ALWAYS_DENIED]
    assert [p.pattern for p in adapter.STORE_COMMAND_TEXT] == [
        p.pattern for p in adapter.SELECTION_STORE] + [guard.BARE_SELECTIONS.pattern,
                                                      guard.GIT_DIR_NAMES.pattern]


@pytest.mark.parametrize("target", ["/r/.git/loom//selections/c.jsonl", "/r/.git/loom/./selections/c.jsonl"])
def test_missing_checker_denies_unnormalised_store_file_target_on_codex(tmp_path, target):
    result = _codex_fallback({"tool_name": "Write", "tool_input": {"file_path": target, "content": "{}"}},
                             tmp_path, matcher=1)
    assert result.returncode == 2 and "BLOCK selection.guard" in result.stderr, result.stderr


@pytest.mark.parametrize("command", ["git status --short", "git log -3 --oneline", "ls -la"])
def test_missing_checker_allows_closed_read_only_set(checkerless_adapter, change_repo, tmp_path, command):
    out = _run("push-gate", _tool_payload(command, ".", [str(change_repo)]), tmp_path,
               adapter=checkerless_adapter)
    assert out["decision"] == "allow"


PARITY_COMMANDS = [
    "git status --short", "git log -3 --oneline", "git -C repo diff --stat", "git branch --list",
    "ls -la", "cat -n README.md", "rg -n --glob=*.py foo", "find . -maxdepth 2 -name x",
    "git push origin feat", "gh pr create --fill", "pytest -q", "git status; rm -rf x",
    "git branch -D feat", "git log --output=x", "find . -delete", "/bin/ls", "cat $(id)",
    "rg --pre=sh foo", "ls -la | sh", "git", "git -C", "echo hi", "cat 'unterminated",
    SELECTION_WRITE, "cat .git/loom/selections/c.jsonl", "ls loom/selections",
]


def test_missing_checker_allow_set_matches_codex_stale_root(checkerless_adapter, change_repo, tmp_path):
    """The agy fallback and the Codex stale-root command decide every command alike."""
    hooks = json.loads((PLUGIN_ROOT / "hooks" / "hooks-codex.json").read_text(encoding="utf-8"))
    codex_command = hooks["hooks"]["PreToolUse"][0]["hooks"][0]["command"]
    empty_root = tmp_path / "stale-root"
    empty_root.mkdir()
    for command in PARITY_COMMANDS:
        agy = _run("push-gate", _tool_payload(command, ".", [str(change_repo)]), tmp_path,
                   adapter=checkerless_adapter)["decision"]
        codex = subprocess.run(
            ["sh", "-c", codex_command],
            input=json.dumps({"tool_name": "Bash", "tool_input": {"command": command}}),
            capture_output=True, text=True, timeout=30,
            env={**os.environ, "PLUGIN_ROOT": str(empty_root)},
        )
        assert codex.returncode in (0, 2), (command, codex.stderr)
        assert agy == ("allow" if codex.returncode == 0 else "deny"), command


def _session_payload(conversation: str) -> dict:
    return {"conversationId": conversation, "workspacePaths": [], "invocationNum": 0,
            "initialNumSteps": 1}


def _user_state_dir(tmp_path: Path, kind: str) -> Path:
    return tmp_path / f"{kind}-{os.getuid()}"


@pytest.mark.skipif(not hasattr(os, "getuid"), reason="per-uid state directory")
def test_marker_dir_is_private_per_user(tmp_path):
    _run("pre-invocation", _session_payload("priv"), tmp_path)
    state = _user_state_dir(tmp_path, "loom-code-agy-session")
    assert (state / "priv").is_file()
    assert state.stat().st_mode & 0o777 == 0o700
    assert not (tmp_path / "loom-code-agy-session").exists()


@pytest.mark.skipif(not hasattr(os, "O_NOFOLLOW") or not hasattr(os, "getuid"),
                    reason="O_NOFOLLOW and per-uid state directory")
def test_marker_symlink_is_not_followed(tmp_path):
    state = _user_state_dir(tmp_path, "loom-code-agy-session")
    state.mkdir(mode=0o700)
    victim = tmp_path / "victim"
    (state / "sym").symlink_to(victim)
    _run("pre-invocation", _session_payload("sym"), tmp_path)
    assert not victim.exists()


@pytest.mark.skipif(not hasattr(os, "getuid"), reason="per-uid state directory")
def test_symlinked_marker_dir_is_not_used(tmp_path):
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    _user_state_dir(tmp_path, "loom-code-agy-session").symlink_to(elsewhere)
    _run("pre-invocation", _session_payload("redir"), tmp_path)
    assert not (elsewhere / "redir").exists()


def test_malformed_tool_payload_denies(tmp_path):
    out = _run("push-gate", {"toolCall": {"name": "run_command", "args": {}}}, tmp_path)
    assert out["decision"] == "deny"


# --- acceptance 5: session context -----------------------------------------

def _invocation(num: int, workspace: list[str], transcript: Path | None = None,
                initial_steps: int = 1, conversation: str = "conv-1") -> dict:
    payload = {"conversationId": conversation, "workspacePaths": workspace, "invocationNum": num,
               "initialNumSteps": initial_steps}
    if transcript is not None:
        payload["transcriptPath"] = str(transcript)
    return payload


def _messages(out: dict) -> list[str]:
    return [step["ephemeralMessage"] for step in out.get("injectSteps", [])]


def test_invocation_zero_injects_station_order(tmp_path):
    workspace = tmp_path / "ws"
    (workspace / "docs" / "loom").mkdir(parents=True)
    (workspace / "docs" / "loom" / "KICKOFF-DEFAULTS.md").write_text("- second-vendor: ask\n")
    out = _run("pre-invocation", _invocation(0, [str(workspace)]), tmp_path)
    (message,) = _messages(out)
    assert "Station order:" in message
    assert "- second-vendor: ask" in message


def test_first_turn_injects(tmp_path):
    out = _run("pre-invocation", _invocation(0, [str(tmp_path)], initial_steps=1), tmp_path)
    (message,) = _messages(out)
    assert "Station order:" in message


def test_second_turn_silent(tmp_path):
    """agy resets invocationNum to 0 on every user turn; initialNumSteps grows."""
    out = _run("pre-invocation", _invocation(0, [str(tmp_path)], initial_steps=3), tmp_path)
    assert out == {}


def test_marker_prevents_repeat(tmp_path):
    first = _run("pre-invocation", _invocation(0, [str(tmp_path)], initial_steps=1), tmp_path)
    again = _run("pre-invocation", _invocation(0, [str(tmp_path)], initial_steps=1), tmp_path)
    other = _run("pre-invocation", _invocation(0, [str(tmp_path)], initial_steps=1,
                                               conversation="conv-2"), tmp_path)
    assert _messages(first)
    assert again == {}
    assert _messages(other)


def test_later_invocations_inject_nothing(tmp_path):
    transcript = _transcript(tmp_path, [_user(EN_TURN)])
    out = _run("pre-invocation", _invocation(4, [str(tmp_path)], transcript), tmp_path)
    assert out == {}


def test_mode_off_injects_nothing(tmp_path):
    out = _run("pre-invocation", _invocation(0, [str(tmp_path)]), tmp_path, LOOM_CODE_MODE="off")
    assert out == {}


# --- acceptance 6: language anchor ------------------------------------------

def _user(text: str) -> dict:
    return {"source": "USER_EXPLICIT", "type": "USER_INPUT",
            "content": f"<USER_REQUEST>\n{text}\n</USER_REQUEST>"}


def _view(path: str) -> dict:
    return {"source": "MODEL", "type": "PLANNER_RESPONSE",
            "tool_calls": [{"name": "view_file", "args": {"AbsolutePath": path}}]}


def _transcript(tmp_path: Path, steps: list[dict]) -> Path:
    path = tmp_path / "transcript_full.jsonl"
    with path.open("w", encoding="utf-8") as fh:
        for index, step in enumerate(steps):
            fh.write(json.dumps({"step_index": index, **step}, ensure_ascii=False) + "\n")
    return path


def test_ja_skill_read_injects_anchor(tmp_path):
    transcript = _transcript(tmp_path, [_user(JA_TURN), _view(LOOM_SKILL)])
    out = _run("pre-invocation", _invocation(1, [str(tmp_path)], transcript), tmp_path)
    (message,) = _messages(out)
    assert JA_FRAGMENT in message


def test_zh_skill_read_injects_anchor(tmp_path):
    transcript = _transcript(tmp_path, [_user(ZH_TURN), _view(LOOM_SKILL)])
    out = _run("pre-invocation", _invocation(1, [str(tmp_path)], transcript), tmp_path)
    (message,) = _messages(out)
    assert ZH_FRAGMENT in message


def test_english_session_silent(tmp_path):
    transcript = _transcript(tmp_path, [_user(EN_TURN), _view(LOOM_SKILL)])
    out = _run("pre-invocation", _invocation(1, [str(tmp_path)], transcript), tmp_path)
    assert out == {}


def test_non_loom_skill_read_silent(tmp_path):
    other = "/Users/u/.gemini/config/plugins/other/skills/x/SKILL.md"
    transcript = _transcript(tmp_path, [_user(JA_TURN), _view(other)])
    out = _run("pre-invocation", _invocation(1, [str(tmp_path)], transcript), tmp_path)
    assert out == {}


def test_anchor_fires_once_per_skill_read_step(tmp_path):
    transcript = _transcript(tmp_path, [_user(JA_TURN), _view(LOOM_SKILL)])
    first = _run("pre-invocation", _invocation(1, [str(tmp_path)], transcript), tmp_path)
    second = _run("pre-invocation", _invocation(2, [str(tmp_path)], transcript), tmp_path)
    assert _messages(first)
    assert second == {}


def test_anchor_not_repeated_by_later_steps_in_same_turn(tmp_path):
    """Later steps in the same turn keep the same latest skill read: no second anchor."""
    steps = [_user(JA_TURN), _view(LOOM_SKILL)]
    first = _run("pre-invocation", _invocation(1, [str(tmp_path)], _transcript(tmp_path, steps)), tmp_path)
    steps.append(_view("/ws/README.md"))
    later = _run("pre-invocation", _invocation(2, [str(tmp_path)], _transcript(tmp_path, steps)), tmp_path)
    assert _messages(first)
    assert later == {}


def test_skill_read_before_tool_result_injects_anchor(tmp_path):
    """agy 1.2.2 live shape: the model is invoked after the view_file result step
    (source MODEL, type GENERIC) lands, so the skill read is no longer the newest step."""
    user = {"step_index": 0, "source": "USER_EXPLICIT", "type": "USER_INPUT", "status": "DONE",
            "content": f"<USER_REQUEST>\n{JA_TURN}\n</USER_REQUEST>"}
    result = {"step_index": 3, "source": "MODEL", "type": "GENERIC", "status": "DONE",
              "content": "File Path: `file:///Users/u/.gemini/config/plugins/loom-workflow/skills/"
                         "recap-state/SKILL.md`\nTotal Lines: 143"}
    path = tmp_path / "transcript.jsonl"
    path.write_text(json.dumps(user, ensure_ascii=False) + "\n" + QUOTED_VIEW_LINE + "\n"
                    + json.dumps(result) + "\n", encoding="utf-8")
    out = _run("pre-invocation", _invocation(1, [str(tmp_path)], path), tmp_path)
    (message,) = _messages(out)
    assert JA_FRAGMENT in message


def test_skill_read_in_earlier_user_turn_silent(tmp_path):
    steps = [_user(JA_TURN), _view(LOOM_SKILL),
             {"source": "MODEL", "type": "GENERIC", "content": "skill body"},
             _user(JA_TURN)]
    transcript = _transcript(tmp_path, steps)
    out = _run("pre-invocation", _invocation(3, [str(tmp_path)], transcript), tmp_path)
    assert out == {}


# agy 1.2.2 live shape: ``transcript.jsonl`` stores each tool arg as a JSON
# string literal (the value carries its own quotes); ``transcript_full.jsonl``
# stores it plain. USER_INPUT content is the same plain string in both.
QUOTED_VIEW_LINE = (
    '{"step_index":2,"source":"MODEL","type":"PLANNER_RESPONSE","status":"DONE",'
    '"tool_calls":[{"name":"view_file","args":{"AbsolutePath":'
    '"\\"/Users/u/.gemini/config/plugins/loom-workflow/skills/recap-state/SKILL.md\\"",'
    '"toolAction":"\\"Viewing skill file\\""}}]}'
)


def _quoted_transcript(tmp_path: Path, user_text: str) -> Path:
    user = {"step_index": 0, "source": "USER_EXPLICIT", "type": "USER_INPUT", "status": "DONE",
            "content": f"<USER_REQUEST>\n{user_text}\n</USER_REQUEST>\n<ADDITIONAL_METADATA>\n"
                       "The current local time is: 2026-09-14T10:47:28+08:00.\n</ADDITIONAL_METADATA>"}
    path = tmp_path / "transcript.jsonl"
    path.write_text(json.dumps(user, ensure_ascii=False) + "\n" + QUOTED_VIEW_LINE + "\n", encoding="utf-8")
    return path


def test_quoted_transcript_args_ja_injects_anchor(tmp_path):
    transcript = _quoted_transcript(tmp_path, JA_TURN)
    out = _run("pre-invocation", _invocation(1, [str(tmp_path)], transcript), tmp_path)
    (message,) = _messages(out)
    assert JA_FRAGMENT in message


def test_quoted_transcript_args_english_silent(tmp_path):
    transcript = _quoted_transcript(tmp_path, EN_TURN)
    out = _run("pre-invocation", _invocation(1, [str(tmp_path)], transcript), tmp_path)
    assert out == {}


def test_empty_workspace_session_context_asks_for_add_dir(tmp_path):
    out = _run("pre-invocation", _invocation(0, []), tmp_path)
    (message,) = _messages(out)
    assert "Station order:" in message
    assert "--add-dir" in message


def test_attached_workspace_session_context_has_no_add_dir_note(tmp_path):
    out = _run("pre-invocation", _invocation(0, [str(tmp_path)]), tmp_path)
    (message,) = _messages(out)
    assert "--add-dir" not in message


def test_unreadable_transcript_is_silent(tmp_path):
    out = _run("pre-invocation", _invocation(2, [str(tmp_path)], tmp_path / "missing.jsonl"), tmp_path)
    assert out == {}
