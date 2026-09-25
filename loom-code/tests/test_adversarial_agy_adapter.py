"""Adversarial probes for ``hooks/agy_adapter.py`` (Antigravity CLI hook adapter).

Each probe feeds the adapter hostile, unnormalised, or boundary agy stdin the
way agy 1.2.2 runs it (cwd = plugin root, JSON on stdin, one JSON object on
stdout, exit 0). A probe that fails is a finding against the change; a probe
that passes records an attack the adapter survived.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pytest

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
ADAPTER = PLUGIN_ROOT / "hooks" / "agy_adapter.py"
LOOM_SKILL = "/Users/u/.gemini/config/plugins/loom-code/skills/build/SKILL.md"
JA_TURN = "この変更が仕様に合っているかどうかを確認してください。よろしくお願いします。"


def _run_raw(mode: str, stdin: str, tmp_path: Path, adapter: Path = ADAPTER, timeout: int = 60):
    environ = {k: v for k, v in os.environ.items()
               if k not in ("LOOM_CODE_MODE", "ANTIGRAVITY_CONVERSATION_ID")}
    environ["TMPDIR"] = str(tmp_path)
    result = subprocess.run(
        [sys.executable, str(adapter), mode], input=stdin, capture_output=True, text=True,
        cwd=adapter.parent.parent, env=environ, timeout=timeout,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def _run(mode: str, payload: dict, tmp_path: Path, adapter: Path = ADAPTER, timeout: int = 60):
    return _run_raw(mode, json.dumps(payload), tmp_path, adapter, timeout)


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@example.com", *args],
                   cwd=repo, check=True, capture_output=True)


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


def _push(command: str, cwd, workspace: list[str]) -> dict:
    args = {"CommandLine": command}
    if cwd is not None:
        args["Cwd"] = cwd
    return {"conversationId": "c1", "workspacePaths": workspace,
            "toolCall": {"name": "run_command", "args": args}, "stepIdx": 3}


# --- push gate: dependency failure and hostile stdin -------------------------

@pytest.fixture
def crashing_checker_adapter(tmp_path: Path) -> Path:
    root = tmp_path / "plugin"
    (root / "hooks").mkdir(parents=True)
    (root / "scripts").mkdir()
    shutil.copy2(ADAPTER, root / "hooks" / "agy_adapter.py")
    (root / "scripts" / "loom_checker.py").write_text("import sys\nsys.exit(3)\n")
    return root / "hooks" / "agy_adapter.py"


def test_pushgate_crashing_checker_push_allows_and_says_so(crashing_checker_adapter, change_repo, tmp_path):
    """A checker that exits neither 0 nor 2 allows the push and names the failure."""
    out = _run("push-gate", _push("git push origin feat", ".", [str(change_repo)]), tmp_path,
               adapter=crashing_checker_adapter)
    assert out["decision"] == "allow", out
    assert out["reason"].startswith("loom: publication hook failed (checker exited 3"), out
    assert out["reason"].endswith("; allowing."), out


@pytest.mark.parametrize("command", [
    "echo x >> .git/loom/selections/c.jsonl",
    "git status\ncp forged .git/loom/selections/c.jsonl",
    "bash -c 'tee -a /r/.git/loom/selections/c.jsonl < ev'",
])
def test_pushgate_crashing_checker_selection_store_denies(crashing_checker_adapter, change_repo, tmp_path,
                                                          command):
    """A crashed checker never loosens the selection-store guard."""
    out = _run("push-gate", _push(command, ".", [str(change_repo)]), tmp_path,
               adapter=crashing_checker_adapter)
    assert out["decision"] == "deny", out
    assert "BLOCK selection.guard" in out["reason"]


def test_pushgate_crashing_checker_git_dash_c_status_allows(crashing_checker_adapter, change_repo, tmp_path):
    """The fallback still allows a read-only command (``git -C dir status``)."""
    out = _run("push-gate", _push(f"git -C {change_repo} status --short", ".", [str(change_repo)]),
               tmp_path, adapter=crashing_checker_adapter)
    assert out["decision"] == "allow"


@pytest.fixture
def stub_checker_adapter(tmp_path: Path):
    """An adapter whose checker is a stub with a chosen exit code and output."""
    def make(code: int, stdout: str = "", stderr: str = "") -> Path:
        root = tmp_path / f"stub-{code}"
        (root / "hooks").mkdir(parents=True)
        (root / "scripts").mkdir()
        shutil.copy2(ADAPTER, root / "hooks" / "agy_adapter.py")
        (root / "scripts" / "loom_checker.py").write_text(
            f"import sys\nsys.stdin.read()\nprint({stdout!r})\n"
            f"print({stderr!r}, file=sys.stderr)\nsys.exit({code})\n")
        return root / "hooks" / "agy_adapter.py"
    return make


def test_pushgate_checker_exit_zero_forwards_reminder(stub_checker_adapter, change_repo, tmp_path):
    line = "loom: verification absent (missing: attestation); publishing anyway."
    adapter = stub_checker_adapter(0, json.dumps({"systemMessage": line}), line)
    out = _run("push-gate", _push("git push origin feat", ".", [str(change_repo)]), tmp_path, adapter=adapter)
    assert out == {"decision": "allow", "reason": line}


def test_pushgate_checker_exit_zero_silent_allows_bare(stub_checker_adapter, change_repo, tmp_path):
    out = _run("push-gate", _push("git status", ".", [str(change_repo)]), tmp_path,
               adapter=stub_checker_adapter(0))
    assert out == {"decision": "allow"}


def test_pushgate_checker_exit_two_passes_its_reason(stub_checker_adapter, change_repo, tmp_path):
    reason = "BLOCK selection.guard: names the selection record store"
    out = _run("push-gate", _push("ls .git/loom", ".", [str(change_repo)]), tmp_path,
               adapter=stub_checker_adapter(2, stderr=reason))
    assert out == {"decision": "deny", "reason": reason}


@pytest.mark.parametrize("stdin", ["not json", "", "[]", "null", '{"toolCall": "x"}',
                                   '{"toolCall": {"args": ["git push"]}}'])
def test_pushgate_hostile_stdin_denies(tmp_path, stdin):
    """Non-JSON, non-object, or mistyped stdin denies instead of crashing or allowing."""
    out = _run_raw("push-gate", stdin, tmp_path)
    assert out["decision"] == "deny", (stdin, out)


# --- pre-invocation: session-context marker ----------------------------------

def _invocation(conversation: str = "conv-1", initial_steps=1, transcript: Path | None = None,
                workspace: list[str] | None = None) -> dict:
    payload = {"conversationId": conversation, "workspacePaths": workspace or [],
               "invocationNum": 0, "initialNumSteps": initial_steps}
    if transcript is not None:
        payload["transcriptPath"] = str(transcript)
    return payload


def _messages(out: dict) -> list[str]:
    return [s["ephemeralMessage"] for s in out.get("injectSteps", [])]


def test_session_traversal_conversation_id_stays_in_tempdir(tmp_path):
    """A conversationId like ``../../escape`` never writes a marker outside the tempdir kind dir."""
    out = _run("pre-invocation", _invocation("../../escape"), tmp_path)
    assert any("Station order:" in m for m in _messages(out))
    assert not (tmp_path / "escape").exists()
    assert not (tmp_path.parent / "escape").exists()


@pytest.mark.parametrize("conversation", ["..", "."])
def test_session_dot_conversation_id_injects_once(tmp_path, conversation):
    """A dot-only conversationId still gets a working marker: the second first-turn call is silent."""
    first = _run("pre-invocation", _invocation(conversation), tmp_path)
    again = _run("pre-invocation", _invocation(conversation), tmp_path)
    assert _messages(first)
    assert again == {}, again


@pytest.mark.parametrize("initial_steps", [-5, "1", None, 1.0])
def test_session_mistyped_initial_steps_injects_at_most_once(tmp_path, initial_steps):
    """Negative or mistyped initialNumSteps never re-injects on a repeat call."""
    first = _run("pre-invocation", _invocation(initial_steps=initial_steps), tmp_path)
    again = _run("pre-invocation", _invocation(initial_steps=initial_steps), tmp_path)
    assert again == {} or not _messages(first), (first, again)


def test_session_unwritable_marker_dir_does_not_crash(tmp_path):
    """A marker location that cannot be created still returns valid JSON with the context."""
    if not hasattr(os, "getuid"):
        pytest.skip("per-user marker directory is keyed by os.getuid, unavailable here")
    (tmp_path / f"loom-code-agy-session-{os.getuid()}").write_text("a file where the dir should be")
    out = _run("pre-invocation", _invocation(), tmp_path)
    assert any("Station order:" in m for m in _messages(out))


# --- pre-invocation: transcript failure must not eat the session context -----

def _write_jsonl(path: Path, steps: list) -> Path:
    path.write_text("".join(json.dumps(s, ensure_ascii=False) + "\n" for s in steps), encoding="utf-8")
    return path


def _user(text: str) -> dict:
    return {"source": "USER_EXPLICIT", "type": "USER_INPUT",
            "content": f"<USER_REQUEST>\n{text}\n</USER_REQUEST>"}


def test_session_malformed_tool_args_keeps_first_turn_context(tmp_path):
    """A transcript MODEL step whose tool args are a list (not an object) must not
    suppress the first-turn session context."""
    transcript = _write_jsonl(tmp_path / "t.jsonl", [
        _user(JA_TURN),
        {"source": "MODEL", "type": "PLANNER_RESPONSE",
         "tool_calls": [{"name": "view_file", "args": [LOOM_SKILL]}]},
    ])
    out = _run("pre-invocation", _invocation(transcript=transcript), tmp_path)
    assert any("Station order:" in m for m in _messages(out)), out


def test_session_partial_utf8_transcript_keeps_first_turn_context(tmp_path):
    """agy appends the transcript while hooks run; a read that lands mid multibyte
    character must not suppress the first-turn session context."""
    transcript = tmp_path / "t.jsonl"
    body = json.dumps(_user(JA_TURN), ensure_ascii=False) + "\n"
    transcript.write_bytes(body.encode("utf-8") + '{"content": "日'.encode("utf-8")[:-1])
    out = _run("pre-invocation", _invocation(transcript=transcript), tmp_path)
    assert any("Station order:" in m for m in _messages(out)), out


def test_session_anchor_crash_does_not_burn_marker(tmp_path):
    """If the first call loses the session context to a transcript error, a retry
    in the same first turn with a clean transcript still delivers it."""
    bad = _write_jsonl(tmp_path / "bad.jsonl", [
        _user(JA_TURN),
        {"source": "MODEL", "tool_calls": [{"name": "view_file", "args": [LOOM_SKILL]}]},
    ])
    good = _write_jsonl(tmp_path / "good.jsonl", [_user(JA_TURN)])
    first = _run("pre-invocation", _invocation(transcript=bad), tmp_path)
    retry = _run("pre-invocation", _invocation(transcript=good), tmp_path)
    delivered = _messages(first) + _messages(retry)
    assert any("Station order:" in m for m in delivered), (first, retry)


# --- pre-invocation: language-anchor transcript parsing ----------------------

def _anchor_payload(transcript: Path) -> dict:
    return {"conversationId": "anchor-conv", "workspacePaths": [], "invocationNum": 3,
            "initialNumSteps": 5, "transcriptPath": str(transcript)}


def test_anchor_non_plugin_path_with_loom_segment_silent(tmp_path):
    """A SKILL.md that merely sits under some directory named ``loom-workflow``
    (not a skills tree of an installed loom plugin) does not fire the anchor."""
    transcript = _write_jsonl(tmp_path / "t.jsonl", [
        _user(JA_TURN),
        {"source": "MODEL", "type": "PLANNER_RESPONSE",
         "tool_calls": [{"name": "view_file",
                         "args": {"AbsolutePath": "/Users/u/notes/loom-workflow/SKILL.md"}}]},
    ])
    out = _run("pre-invocation", _anchor_payload(transcript), tmp_path)
    assert out == {}, out


def test_anchor_garbage_lines_still_anchor(tmp_path):
    """Malformed JSONL lines, scalars, and arrays are skipped; the anchor still fires."""
    transcript = tmp_path / "t.jsonl"
    lines = ["{broken", "42", "[1,2]", "null", json.dumps(_user(JA_TURN), ensure_ascii=False),
             json.dumps({"source": "MODEL", "tool_calls": [
                 {"name": "view_file", "args": {"AbsolutePath": LOOM_SKILL}}]})]
    transcript.write_text("\n".join(lines) + "\n", encoding="utf-8")
    out = _run("pre-invocation", _anchor_payload(transcript), tmp_path)
    assert any("日本語" in m for m in _messages(out)), out


def test_anchor_nonstring_user_content_silent_not_crash(tmp_path):
    """USER_INPUT content that is a number or object yields valid JSON, not a crash."""
    transcript = _write_jsonl(tmp_path / "t.jsonl", [
        {"source": "USER_EXPLICIT", "type": "USER_INPUT", "content": 12345},
        {"source": "USER_EXPLICIT", "type": "USER_INPUT", "content": {"x": 1}},
        {"source": "MODEL", "tool_calls": [{"name": "view_file", "args": {"AbsolutePath": LOOM_SKILL}}]},
    ])
    out = _run("pre-invocation", _anchor_payload(transcript), tmp_path)
    assert out == {} or "injectSteps" in out


def test_anchor_huge_transcript_within_hook_timeout(tmp_path):
    """A long conversation (120k steps) finishes well inside the 20 s hook timeout."""
    transcript = tmp_path / "t.jsonl"
    user = json.dumps(_user(JA_TURN), ensure_ascii=False)
    model = json.dumps({"source": "MODEL", "type": "PLANNER_RESPONSE", "content": "ok"})
    with transcript.open("w", encoding="utf-8") as fh:
        for _ in range(60_000):
            fh.write(user + "\n")
            fh.write(model + "\n")
        fh.write(json.dumps({"source": "MODEL", "tool_calls": [
            {"name": "view_file", "args": {"AbsolutePath": LOOM_SKILL}}]}) + "\n")
    started = time.monotonic()
    out = _run("pre-invocation", _anchor_payload(transcript), tmp_path, timeout=120)
    elapsed = time.monotonic() - started
    assert elapsed < 15, f"pre-invocation took {elapsed:.1f}s on a 120k-step transcript"
    assert any("日本語" in m for m in _messages(out)), out
